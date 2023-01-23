terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.50.0"
    }
  }
}

provider "aws" {
  access_key = var.aws.access_key
  secret_key = var.aws.secret_key
  region     = var.aws.region

  s3_use_path_style           = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3       = var.aws.endpoint.s3
    lambda   = var.aws.endpoint.lambda
    sqs      = var.aws.endpoint.sqs
    sns      = var.aws.endpoint.sns
    dynamodb = var.aws.endpoint.dynamodb
  }
}
