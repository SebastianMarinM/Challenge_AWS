import boto3
import time
import pandas as pd
from botocore.exceptions import ClientError

class AthenaQuerier:
    def __init__(self, database, s3_output_location):
        self.athena_client = boto3.client('athena')
        self.s3_client = boto3.client('s3')
        self.database = database
        self.s3_output_location = s3_output_location

    def run_query(self, query):
        try:
            # Start the query execution
            response = self.athena_client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': self.database},
                ResultConfiguration={'OutputLocation': self.s3_output_location}
            )
            query_execution_id = response['QueryExecutionId']

            # Wait for the query to complete
            while True:
                response = self.athena_client.get_query_execution(QueryExecutionId=query_execution_id)
                state = response['QueryExecution']['Status']['State']
                
                if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                time.sleep(1)

            if state == 'SUCCEEDED':
                # Get the results
                results = self.athena_client.get_query_results(QueryExecutionId=query_execution_id)
                return self._process_results(results)
            else:
                error = response['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
                raise Exception(f"Query failed: {error}")

        except ClientError as e:
            print(f"Error executing query: {e}")
            raise

    def _process_results(self, results):
        # Extract column names
        columns = [col['Label'] for col in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        
        # Extract data rows
        rows = []
        for row in results['ResultSet']['Rows'][1:]:  # Skip header row
            rows.append([field.get('VarCharValue', '') for field in row['Data']])
        
        # Create pandas DataFrame
        return pd.DataFrame(rows, columns=columns)

def main():
    # Initialize the querier
    querier = AthenaQuerier(
        database='energy_trading',
        s3_output_location='s3://your-bucket/athena-results/'
    )

    # Example queries for challenge
    queries = {
        'provider_summary': """
        SELECT 
            energy_type,
            COUNT(*) as provider_count,
            AVG(capacity_mw) as avg_capacity
        FROM providers
        GROUP BY energy_type
        """,
        
        'transaction_summary': """
        SELECT 
            t.transaction_type,
            t.energy_type,
            COUNT(*) as transaction_count,
            SUM(quantity_kwh) as total_quantity,
            AVG(price_per_kwh) as avg_price
        FROM transactions t
        GROUP BY t.transaction_type, t.energy_type
        """,
        
        'customer_transactions': """
        SELECT 
            c.customer_type,
            c.city,
            COUNT(t.transaction_id) as transaction_count,
            SUM(t.total_amount) as total_amount
        FROM customers c
        JOIN transactions t ON c.customer_id = t.entity_id
        WHERE t.transaction_type = 'sell'
        GROUP BY c.customer_type, c.city
        """
    }

    # Execute queries and print results
    for query_name, query in queries.items():
        print(f"\nExecuting {query_name}...")
        try:
            results = querier.run_query(query)
            print(f"\nResults for {query_name}:")
            print(results)
        except Exception as e:
            print(f"Error executing {query_name}: {e}")

if __name__ == "__main__":
    main() 