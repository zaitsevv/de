variable "aws" {
  type = object({
    access_key = string
    secret_key = string
    region     = string
    endpoint   = map(string)
  })
  default = {
    access_key = "mock_access_key"
    secret_key = "mock_secret_key"
    region     = "eu-north-1"
    endpoint   = {
      s3       = "http://10.5.0.2:4566"
      lambda   = "http://10.5.0.2:4566"
      sqs      = "http://10.5.0.2:4566"
      sns      = "http://10.5.0.2:4566"
      dynamodb = "http://10.5.0.2:4566"
    }
  }
}

variable "dynamodb" {
  type = object({
    capacity = map(number)
  })
  default = {
    capacity = {
      read  = 10
      write = 10
    }
  }
}

variable "lambda" {
  type = object({
    directory = string
    role = string
    runtime = string
    timeout = number
  })
  default = {
    directory = "../lambdas"
    role = "mock_role"
    runtime = "python3.9"
    timeout = 900
  }
}
