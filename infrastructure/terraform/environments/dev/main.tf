locals {
  environment = "dev"
  project     = "energy-trading"
  region      = "us-east-1"
}

module "s3" {
  source = "../../modules/s3"

  bucket_name = "${local.project}-${local.environment}-datalake"
  environment = local.environment
  tags = {
    Project     = local.project
    Environment = local.environment
  }
}

module "glue" {
  source = "../../modules/glue"

  environment      = local.environment
  data_lake_bucket = module.s3.bucket_name
  tags = {
    Project     = local.project
    Environment = local.environment
  }
}

# Lake Formation configuration
resource "aws_lakeformation_data_lake_settings" "settings" {
  admins = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/admin"]
}

resource "aws_lakeformation_resource" "s3" {
  arn = module.s3.bucket_arn
}

# Redshift cluster for data warehouse
resource "aws_redshift_cluster" "warehouse" {
  cluster_identifier = "${local.project}-${local.environment}"
  database_name     = "energy_trading"
  master_username   = "admin"
  master_password   = var.redshift_password
  node_type        = "dc2.large"
  cluster_type     = "single-node"
  
  skip_final_snapshot = true
  
  vpc_security_group_ids = [aws_security_group.redshift.id]
  
  tags = {
    Project     = local.project
    Environment = local.environment
  }
}

# Security group for Redshift
resource "aws_security_group" "redshift" {
  name_prefix = "${local.project}-${local.environment}-redshift"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  tags = {
    Project     = local.project
    Environment = local.environment
  }
}

# Data source for current AWS account
data "aws_caller_identity" "current" {} 