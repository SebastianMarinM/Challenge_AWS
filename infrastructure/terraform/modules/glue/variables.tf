variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "data_lake_bucket" {
  description = "Name of the S3 bucket containing the data lake"
  type        = string
}

variable "tags" {
  description = "Additional tags for Glue resources"
  type        = map(string)
  default     = {}
} 