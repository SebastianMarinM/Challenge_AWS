provider "aws" {
  region = "us-east-1"
  
  default_tags {
    tags = {
      Environment = "dev"
      Project     = "energy-trading-datalake"
      ManagedBy   = "terraform"
    }
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "s3" {
    bucket = "energy-trading-tfstate"
    key    = "dev/terraform.tfstate"
    region = "us-east-1"
  }

  required_version = ">= 1.0.0"
} 