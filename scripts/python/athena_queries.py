import boto3
import time
import pandas as pd
from botocore.exceptions import ClientError

class AthenaClient:
    def __init__(self, database, s3_output_location):
        self.athena = boto3.client('athena')
        self.s3 = boto3.client('s3')
        self.database = database
        self.s3_output_location = s3_output_location

    def run_query(self, query):
        try:
            response = self.athena.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': self.database},
                ResultConfiguration={'OutputLocation': self.s3_output_location}
            )
            query_execution_id = response['QueryExecutionId']
            
            # Wait for query to complete
            while True:
                response = self.athena.get_query_execution(QueryExecutionId=query_execution_id)
                state = response['QueryExecution']['Status']['State']
                
                if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                time.sleep(1)
            
            if state == 'SUCCEEDED':
                results = self.athena.get_query_results(QueryExecutionId=query_execution_id)
                return self._process_results(results)
            else:
                error = response['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
                raise Exception(f"Query failed: {error}")
                
        except ClientError as e:
            raise Exception(f"AWS Error: {str(e)}")

    def _process_results(self, results):
        columns = [col['Label'] for col in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        rows = []
        
        for row in results['ResultSet']['Rows'][1:]:  # Skip header
            values = [field.get('VarCharValue', '') for field in row['Data']]
            rows.append(dict(zip(columns, values)))
            
        return pd.DataFrame(rows)

def main():
    # Initialize Athena client
    athena_client = AthenaClient(
        database='energy_trading_db',
        s3_output_location='s3://your-athena-output-bucket/results/'
    )

    # Example queries
    queries = {
        'total_energy_by_type': """
            SELECT 
                energy_type,
                SUM(quantity_kwh) as total_energy,
                AVG(price_per_kwh) as avg_price
            FROM transactions
            WHERE transaction_type = 'venta'
            GROUP BY energy_type
            ORDER BY total_energy DESC
        """,
        
        'top_clients': """
            SELECT 
                c.client_name,
                c.client_type,
                COUNT(*) as transaction_count,
                SUM(t.quantity_kwh) as total_energy_consumed,
                SUM(t.total_amount) as total_spent
            FROM transactions t
            JOIN clients c ON t.entity_id = c.client_id
            WHERE t.transaction_type = 'venta'
            GROUP BY c.client_name, c.client_type
            ORDER BY total_spent DESC
            LIMIT 10
        """,
        
        'provider_performance': """
            SELECT 
                p.provider_name,
                p.energy_type,
                COUNT(*) as sales_count,
                SUM(t.quantity_kwh) as total_energy_sold,
                AVG(t.price_per_kwh) as avg_price
            FROM transactions t
            JOIN providers p ON t.entity_id = p.provider_id
            WHERE t.transaction_type = 'compra'
            GROUP BY p.provider_name, p.energy_type
            ORDER BY total_energy_sold DESC
        """
    }

    # Execute queries and print results
    for query_name, query in queries.items():
        print(f"\nExecuting query: {query_name}")
        try:
            results = athena_client.run_query(query)
            print("\nResults:")
            print(results)
        except Exception as e:
            print(f"Error executing query {query_name}: {str(e)}")

if __name__ == "__main__":
    main()
