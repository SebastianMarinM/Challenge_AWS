import boto3
import os
from datetime import datetime

def upload_to_s3(local_file, bucket, s3_key):
    """Upload a file to S3"""
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(local_file, bucket, s3_key)
        print(f"Successfully uploaded {local_file} to s3://{bucket}/{s3_key}")
    except Exception as e:
        print(f"Error uploading {local_file}: {str(e)}")

def main():
    # Configuration
    bucket_name = "your-energy-trading-datalake"  # Replace with your bucket name
    timestamp = datetime.now().strftime('%Y%m%d')
    
    # Define the files to upload
    files = [
        ("providers", f"data/raw/providers_{timestamp}.csv"),
        ("customers", f"data/raw/customers_{timestamp}.csv"),
        ("transactions", f"data/raw/transactions_{timestamp}.csv")
    ]
    
    # Upload each file to the appropriate S3 location
    for entity, local_path in files:
        if os.path.exists(local_path):
            s3_key = f"landing/{entity}/year={timestamp[:4]}/month={timestamp[4:6]}/day={timestamp[6:8]}/{os.path.basename(local_path)}"
            upload_to_s3(local_path, bucket_name, s3_key)
        else:
            print(f"File not found: {local_path}")

if __name__ == "__main__":
    main() 