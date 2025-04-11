# Energy Trading Data Lake Project

## Overview
This project implements a data lake solution for an energy trading company using AWS services. The solution processes data from providers, customers, and transactions, implementing a robust ETL pipeline with proper data governance.

## Architecture
The project follows a multi-layer data lake architecture:
- Landing Zone: Raw CSV files from source systems
- Raw Zone: Validated and partitioned data
- Transform Zone: Processed data in Parquet format
- Analytics Zone: Optimized data for querying

## Key Components
- AWS S3 for data storage
- AWS Glue for ETL processes and data catalog
- AWS Lake Formation for data governance
- Amazon Athena for SQL queries
- Terraform for Infrastructure as Code

## Prerequisites
- AWS CLI configured
- Terraform >= 1.0.0
- Python >= 3.8
- AWS Account with appropriate permissions

## Project Structure
```
.
├── infrastructure/          # IaC resources
│   └── terraform/
│       ├── modules/        # Reusable Terraform modules
│       └── environments/   # Environment configurations
├── src/
│   ├── etl/               # ETL scripts and Glue jobs
│   ├── utils/             # Utility functions
│   ├── sql/              # Athena queries
│   └── scripts/          # General purpose scripts
├── data/                 # Sample data
├── tests/               # Test suite
└── docs/               # Documentation
```

## Setup Instructions
1. Configure AWS credentials
2. Initialize Terraform:
   ```bash
   cd infrastructure/terraform/environments/dev
   terraform init
   terraform plan
   terraform apply
   ```
3. Deploy ETL jobs:
   ```bash
   python src/scripts/deploy_glue_jobs.py
   ```

## Data Model
The solution processes three main entities:
1. Providers (CSV):
   - Provider name
   - Energy type (wind, hydro, nuclear)
   - Additional metadata

2. Customers (CSV):
   - ID type
   - ID number
   - Name
   - City

3. Transactions (CSV):
   - Transaction type (buy/sell)
   - Customer/Provider name
   - Quantity
   - Price
   - Energy type

## Security
- AWS Lake Formation for fine-grained access control
- S3 bucket encryption
- IAM roles and policies
- VPC configuration for network isolation

## Monitoring
- CloudWatch metrics and logs
- Glue job monitoring
- Data quality checks

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
MIT License 