variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-central-1" # Frankfurt region, change as needed
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "job-market-pipeline"
}

# S3 Variables
variable "raw_data_bucket_name" {
  description = "Name of the S3 bucket for raw data"
  type        = string
  default     = "stepstone-raw-data"
}

# Redshift Variables
variable "redshift_cluster_identifier" {
  description = "Identifier for the Redshift cluster"
  type        = string
  default     = "job-market-warehouse"
}

variable "redshift_database_name" {
  description = "Name of the Redshift database"
  type        = string
  default     = "jobmarketdb"
}

variable "redshift_master_username" {
  description = "Master username for Redshift cluster"
  type        = string
  default     = "admin"
}

variable "redshift_master_password" {
  description = "Master password for Redshift cluster"
  type        = string
  sensitive   = true
  # Don't set a default for passwords, provide via command line or environment variable
}

variable "redshift_node_type" {
  description = "Node type for Redshift cluster"
  type        = string
  default     = "dc2.large" # Smallest node type, use in development
}

variable "redshift_number_of_nodes" {
  description = "Number of nodes in Redshift cluster"
  type        = number
  default     = 1
}
