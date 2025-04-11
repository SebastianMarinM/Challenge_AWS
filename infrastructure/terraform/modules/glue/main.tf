resource "aws_glue_catalog_database" "energy_trading" {
  name = "${var.environment}_energy_trading"
}

# Glue Crawler for raw data
resource "aws_glue_crawler" "raw_data" {
  database_name = aws_glue_catalog_database.energy_trading.name
  name          = "${var.environment}_raw_data_crawler"
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${var.data_lake_bucket}/raw/"
  }

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }

  configuration = jsonencode({
    Version = 1.0
    CrawlerOutput = {
      Partitions = { AddOrUpdateBehavior = "InheritFromTable" }
    }
  })
}

# Glue Jobs for data transformation
resource "aws_glue_job" "transform_providers" {
  name     = "${var.environment}_transform_providers"
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${var.data_lake_bucket}/scripts/transform_providers.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"               = "python"
    "--continuous-log-logGroup"    = "/aws-glue/jobs/${var.environment}_transform_providers"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"            = "true"
  }
}

resource "aws_glue_job" "transform_customers" {
  name     = "${var.environment}_transform_customers"
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${var.data_lake_bucket}/scripts/transform_customers.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"               = "python"
    "--continuous-log-logGroup"    = "/aws-glue/jobs/${var.environment}_transform_customers"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"            = "true"
  }
}

resource "aws_glue_job" "transform_transactions" {
  name     = "${var.environment}_transform_transactions"
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://${var.data_lake_bucket}/scripts/transform_transactions.py"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"               = "python"
    "--continuous-log-logGroup"    = "/aws-glue/jobs/${var.environment}_transform_transactions"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"            = "true"
  }
}

# IAM Role for Glue
resource "aws_iam_role" "glue_role" {
  name = "${var.environment}_glue_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# Attach AWS managed policy for Glue
resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Custom policy for S3 access
resource "aws_iam_role_policy" "glue_s3_access" {
  name = "${var.environment}_glue_s3_access"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${var.data_lake_bucket}",
          "arn:aws:s3:::${var.data_lake_bucket}/*"
        ]
      }
    ]
  })
} 