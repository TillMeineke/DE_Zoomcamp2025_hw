# S3 bucket for raw data
resource "aws_s3_bucket" "raw_data" {
  bucket = "${var.project_name}-${var.raw_data_bucket_name}-${var.environment}"

  lifecycle {
    prevent_destroy = true
  }
}

# Enable versioning for the bucket (optional but recommended)
resource "aws_s3_bucket_versioning" "raw_data_versioning" {
  bucket = aws_s3_bucket.raw_data.id
  versioning_configuration {
    status = "Enabled"
  }
}

# S3 bucket folder structure
resource "aws_s3_object" "raw_folder" {
  bucket = aws_s3_bucket.raw_data.id
  key    = "raw/"
  content_type = "application/x-directory"
}

resource "aws_s3_object" "stepstone_folder" {
  bucket = aws_s3_bucket.raw_data.id
  key    = "raw/stepstone/"
  content_type = "application/x-directory"
}

# Athena workgroup
resource "aws_athena_workgroup" "job_analysis" {
  name = "${var.project_name}-${var.environment}"

  configuration {
    enforce_workgroup_configuration = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.raw_data.bucket}/athena-results/"
    }
  }
}

# Athena database
resource "aws_athena_database" "job_database" {
  name   = "${replace(var.project_name, "-", "_")}_${var.environment}"
  bucket = aws_s3_bucket.raw_data.bucket
}

# Redshift security group
resource "aws_security_group" "redshift" {
  name        = "${var.project_name}-redshift-${var.environment}"
  description = "Allow inbound traffic to Redshift"

  ingress {
    description = "Access to Redshift"
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # In production, restrict to your IP or VPC
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# IAM role for Redshift
resource "aws_iam_role" "redshift_role" {
  name = "${var.project_name}-redshift-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      }
    ]
  })
}

# Attach policy to allow Redshift to access S3
resource "aws_iam_role_policy_attachment" "redshift_s3_access" {
  role       = aws_iam_role.redshift_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

# Redshift cluster
resource "aws_redshift_cluster" "job_warehouse" {
  cluster_identifier        = "${var.redshift_cluster_identifier}-${var.environment}"
  database_name             = var.redshift_database_name
  master_username           = var.redshift_master_username
  master_password           = var.redshift_master_password
  node_type                 = var.redshift_node_type
  cluster_type              = var.redshift_number_of_nodes > 1 ? "multi-node" : "single-node"
  number_of_nodes           = var.redshift_number_of_nodes
  skip_final_snapshot       = true # For development; set to false in production
  publicly_accessible       = true # For development; set to false in production
  vpc_security_group_ids    = [aws_security_group.redshift.id]
  iam_roles                 = [aws_iam_role.redshift_role.arn]

  # Enhanced VPC routing - enables Redshift traffic through VPC
  enhanced_vpc_routing = true
}
