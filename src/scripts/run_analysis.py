import boto3
import pandas as pd
import time
from datetime import datetime
import os

class EnergyAnalyzer:
    def __init__(self, database, output_bucket):
        self.athena = boto3.client('athena')
        self.s3 = boto3.client('s3')
        self.database = database
        self.output_bucket = output_bucket
        self.output_path = f"s3://{output_bucket}/athena_results/"
        
    def run_query(self, query, output_file):
        """Execute Athena query and wait for results"""
        query_response = self.athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': self.database},
            ResultConfiguration={'OutputLocation': self.output_path}
        )
        
        execution_id = query_response['QueryExecutionId']
        state = 'RUNNING'
        
        while state in ['RUNNING', 'QUEUED']:
            response = self.athena.get_query_execution(QueryExecutionId=execution_id)
            state = response['QueryExecution']['Status']['State']
            
            if state == 'FAILED':
                raise Exception(response['QueryExecution']['Status']['StateChangeReason'])
            elif state == 'SUCCEEDED':
                results = self.athena.get_query_results(QueryExecutionId=execution_id)
                self._save_results(results, output_file)
                return True
                
            time.sleep(1)
    
    def _save_results(self, results, output_file):
        """Convert Athena results to DataFrame and save to CSV"""
        columns = [col['Label'] for col in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
        data = []
        
        for row in results['ResultSet']['Rows'][1:]:  # Skip header
            data.append([field.get('VarCharValue', '') for field in row['Data']])
            
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

def main():
    # Configuration
    database = "energy_trading"
    output_bucket = "your-energy-trading-datalake"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = "analysis_results"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize analyzer
    analyzer = EnergyAnalyzer(database, output_bucket)
    
    # Define analyses to run
    analyses = {
        'customer_consumption': """
            SELECT 
                customer_type,
                city,
                COUNT(DISTINCT customer_id) as customer_count,
                SUM(total_energy_purchased) as total_energy,
                AVG(avg_price_per_kwh) as avg_price
            FROM 
                customer_analysis
            GROUP BY 
                customer_type,
                city
            ORDER BY 
                total_energy DESC
        """,
        
        'provider_performance': """
            SELECT 
                region,
                energy_type,
                COUNT(DISTINCT provider_id) as provider_count,
                SUM(total_energy_sold) as total_energy_sold,
                AVG(avg_price_per_kwh) as avg_price
            FROM 
                provider_analysis
            GROUP BY 
                region,
                energy_type
            ORDER BY 
                total_energy_sold DESC
        """,
        
        'energy_trends': """
            SELECT 
                energy_type,
                month,
                SUM(total_energy) as total_energy,
                AVG(avg_price) as avg_price
            FROM 
                energy_type_analysis
            WHERE 
                month >= DATE_ADD('month', -6, CURRENT_DATE)
            GROUP BY 
                energy_type,
                month
            ORDER BY 
                month DESC,
                energy_type
        """
    }
    
    # Run each analysis
    for name, query in analyses.items():
        output_file = os.path.join(output_dir, f"{name}_{timestamp}.csv")
        print(f"\nRunning analysis: {name}")
        try:
            analyzer.run_query(query, output_file)
        except Exception as e:
            print(f"Error running {name}: {str(e)}")

if __name__ == "__main__":
    main() 