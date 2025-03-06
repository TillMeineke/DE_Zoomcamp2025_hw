# Job Market Data Pipeline

## Project Overview

This project creates an end-to-end data pipeline for scraping, processing, and analyzing job postings from Stepstone. The goal is to build a comprehensive dataset of job listings with detailed attributes to enable insights about the job market, particularly focusing on data-related roles in Hamburg, Germany.

## Problem Statement

Finding relevant job opportunities in the data field requires searching through multiple job portals and analyzing numerous listings. This project aims to:

1. Automate the collection of job postings from Stepstone
2. Standardize and clean the collected data
3. Store the data in a structured database
4. Provide analytics on job trends, required skills, salary distributions, etc.
5. Create visualizations to better understand the job market

## Architecture

The pipeline consists of the following components:

1. **Data Collection**: Web scraper for Stepstone
2. **Data Storage**: AWS S3 for raw data, AWS Athena for querying, AWS Redshift for structured storage
3. **Data Processing**: dlt for ingestion, dbt for transformation
4. **Orchestration**: Kestra for workflow management
5. **Visualization**: Metabase for dashboards

## Dataset

The dataset contains job listings with attributes including:

- Job title and description
- Company information
- Location
- Salary information (when available)
- Required skills
- Employment type (full-time, part-time, etc.)
- Remote work options
- Date posted

## Setup and Installation

### Prerequisites

- Python 3.11.8
- AWS account
- Docker
- Terraform

### Installation Steps

```bash
# Clone the repository
git clone <repository-url>
cd job-market-data-pipeline

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

The project uses several configuration files for different components:

1. **Environment Variables**: Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
# Edit .env with your configuration
```

2. **Terraform Variables**: For infrastructure deployment:

```bash
# Copy example file
cp infrastructure/terraform/terraform.tfvars.example infrastructure/terraform/terraform.tfvars
# Edit with your specific values
```

3. **Environment Setup Script**: For setting Terraform environment variables:

```bash
# Copy example script
cp infrastructure/terraform/set_env.sh.example infrastructure/terraform/set_env.sh
# Edit with your credentials
chmod +x infrastructure/terraform/set_env.sh
source infrastructure/terraform/set_env.sh
```

## Usage

### Running the Scraper

The scraper is implemented in Python:

```bash
cd scraper
python stepstone.py
```

### Running the Pipeline

The pipeline is orchestrated using Kestra:

```bash
# Start Kestra
docker-compose up -d

# Deploy workflows
kestra deployments create --from ./pipeline/kestra_workflows
```

### Deploying Infrastructure

Infrastructure is managed with Terraform:

```bash
cd infrastructure/terraform

# Option 1: Using terraform.tfvars
terraform init
terraform plan
terraform apply

# Option 2: Using environment variables
source set_env.sh
terraform init
terraform plan
terraform apply
```

### CI/CD Pipeline

The project includes GitHub Actions workflows for CI/CD. To set it up:

1. Add required secrets to your GitHub repository:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - All required `TF_VAR_*` variables

2. The workflow will automatically run on pushes to the main branch or pull requests that modify Terraform files.

### Database Schema

The database schema is managed with dbt:

```bash
cd dbt
dbt run
```

## Project Structure

```
stepstone-pipeline/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── terraform-deploy.yml
├── scraper/
│   ├── stepstone.py
│   └── helpers.py
├── pipeline/
│   ├── dlt_ingestion/
│   └── kestra_workflows/
├── dbt/
│   ├── models/
│   ├── analyses/
│   └── tests/
├── dashboard/
│   └── metabase_configs/
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars.example
│   │   ├── set_env.sh.example
│   │   └── README.md
│   └── kubernetes/
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── .gitignore
└── README.md
```

## Future Enhancements

- Add more job portals (LinkedIn, Indeed, etc.)
- Implement automated scheduled scraping
- Create a REST API for querying job data
- Develop ML models for job recommendation
- Build a web interface for exploring job data

## Technology Stack

- **Programming Language**: Python
- **Data Processing**: Pandas, NumPy
- **Web Scraping**: BeautifulSoup4, Scrapy
- **Data Storage**: AWS S3, AWS Athena, AWS Redshift
- **Orchestration**: Kestra
- **Transformation**: dbt
- **Infrastructure as Code**: Terraform
- **CI/CD**: GitHub Actions
- **Visualization**: Metabase

## Security Best Practices

- All sensitive configuration files are added to `.gitignore`
- Example configuration files are provided without sensitive data
- Environment variables are used for CI/CD pipelines
- Infrastructure credentials are never stored in the code
- Following the principle of least privilege for AWS IAM roles

## License

[License information]

## Contributing

[Contribution guidelines]
