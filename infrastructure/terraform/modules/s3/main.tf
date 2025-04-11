resource "aws_s3_bucket" "data_lake" {
  bucket = var.bucket_name

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Create folders for different data lake zones
resource "aws_s3_object" "landing_zone" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "landing/"
  source = "/dev/null"
}

resource "aws_s3_object" "raw_zone" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "raw/"
  source = "/dev/null"
}

resource "aws_s3_object" "processed_zone" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "processed/"
  source = "/dev/null"
}

resource "aws_s3_object" "analytics_zone" {
  bucket = aws_s3_bucket.data_lake.id
  key    = "analytics/"
  source = "/dev/null"
} 