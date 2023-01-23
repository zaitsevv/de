resource "aws_s3_bucket" "helsinki-city-bikes-bucket" {
  bucket = "helsinki-city-bikes"
}

resource "aws_dynamodb_table" "helsinki-city-bikes-raw-table" {
  name           = "helsinki_city_bikes_raw"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "departure_id"
  range_key      = "return_id"
  attribute {
    name = "departure_id"
    type = "N"
  }
  attribute {
    name = "return_id"
    type = "N"
  }
}

resource "aws_dynamodb_table" "helsinki-city-bikes-station_metrics-table" {
  name           = "helsinki_city_bikes_station_metrics"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "station_name"
  attribute {
    name = "station_name"
    type = "S"
  }
}

resource "aws_dynamodb_table" "helsinki-city-bikes-daily-metrics-table" {
  name           = "helsinki_city_bikes_daily_metrics"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "date"
  attribute {
    name = "date"
    type = "S"
  }
}

resource "aws_dynamodb_table" "helsinki-city-bikes-monthly-metrics-table" {
  name           = "helsinki_city_bikes_monthly_metrics"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "date"
  attribute {
    name = "date"
    type = "S"
  }
}

resource "aws_sqs_queue" "helsinki-city-bikes-metrics-object-created-notifications-queue" {
  name = "helsinki_city_bikes_metrics_object_created_notifications"
}

resource "aws_sns_topic" "helsinki-city-bikes-object-created-notifications-topic" {
  name = "helsinki_city_bikes_object_created_notifications"
}

resource "aws_lambda_function" "load-file-to-raw-table-lambda" {
  function_name = "load_file_to_raw_table"
  role          = var.lambda.role
  filename      = "${var.lambda.directory}/load_file_to_raw_table.zip"
  handler       = "load_file_to_raw_table.lambda_handler"
  runtime       = var.lambda.runtime
  timeout       = var.lambda.timeout
  environment {
    variables = {
      AWS_ENDPOINT_URL = var.aws.endpoint.lambda
      AWS_ACCESS_KEY   = var.aws.access_key
      AWS_SECRET_KEY   = var.aws.secret_key
      AWS_REGION_NAME  = var.aws.region
    }
  }
}

resource "aws_lambda_function" "load-file-to-station-metrics-table-lambda" {
  function_name = "load_file_to_station_metrics_table"
  role          = var.lambda.role
  handler       = "load_file_to_station_metrics_table.lambda_handler"
  filename      = "${var.lambda.directory}/load_file_to_station_metrics_table.zip"
  runtime       = var.lambda.runtime
  timeout       = var.lambda.timeout
  environment {
    variables = {
      AWS_ENDPOINT_URL = var.aws.endpoint.lambda
      AWS_ACCESS_KEY   = var.aws.access_key
      AWS_SECRET_KEY   = var.aws.secret_key
      AWS_REGION_NAME  = var.aws.region
    }
  }
}

resource "aws_lambda_function" "load-file-to-daily-metrics-table-lambda" {
  function_name = "load_data_to_daily_metrics_table"
  role          = var.lambda.role
  filename      = "${var.lambda.directory}/load_file_to_daily_metrics_table.zip"
  handler       = "load_file_to_daily_metrics_table.lambda_handler"
  runtime       = var.lambda.runtime
  timeout       = var.lambda.timeout
  environment {
    variables = {
      AWS_ENDPOINT_URL = var.aws.endpoint.lambda
      AWS_ACCESS_KEY   = var.aws.access_key
      AWS_SECRET_KEY   = var.aws.secret_key
      AWS_REGION_NAME  = var.aws.region
    }
  }
}

resource "aws_lambda_function" "load-file-to-monthly-metrics-table-lambda" {
  function_name = "load_data_to_monthly_metrics_table"
  role          = var.lambda.role
  filename      = "${var.lambda.directory}/load_file_to_monthly_metrics_table.zip"
  handler       = "load_file_to_monthly_metrics_table.lambda_handler"
  runtime       = var.lambda.runtime
  timeout       = var.lambda.timeout
  environment {
    variables = {
      AWS_ENDPOINT_URL = var.aws.endpoint.lambda
      AWS_ACCESS_KEY   = var.aws.access_key
      AWS_SECRET_KEY   = var.aws.secret_key
      AWS_REGION_NAME  = var.aws.region
    }
  }
}

resource "aws_s3_bucket_notification" "helsinki-city-bikes-object-created-notification" {
  bucket = aws_s3_bucket.helsinki-city-bikes-bucket.bucket
  queue {
    queue_arn     = aws_sqs_queue.helsinki-city-bikes-metrics-object-created-notifications-queue.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "metrics"
    filter_suffix = ".csv"
  }
  topic {
    topic_arn     = aws_sns_topic.helsinki-city-bikes-object-created-notifications-topic.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "data"
    filter_suffix = ".csv"
  }
}

resource "aws_lambda_event_source_mapping" "s3-metrics-object-created-event-load-file-to-station-metrics-table-lambda-mapping" {
  function_name    = aws_lambda_function.load-file-to-station-metrics-table-lambda.arn
  event_source_arn = aws_sqs_queue.helsinki-city-bikes-metrics-object-created-notifications-queue.arn
}

resource "aws_sns_topic_subscription" "s3-object-created-notification-load-file-to-raw-table-lambda-subscription" {
  topic_arn = aws_sns_topic.helsinki-city-bikes-object-created-notifications-topic.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.load-file-to-raw-table-lambda.arn
}

resource "aws_sns_topic_subscription" "s3-object-created-notification-load-file-to-daily-metrics-table-lambda-subscription" {
  topic_arn = aws_sns_topic.helsinki-city-bikes-object-created-notifications-topic.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.load-file-to-daily-metrics-table-lambda.arn
}

resource "aws_sns_topic_subscription" "s3-object-created-notification-load-file-to-monthly-metrics-table-lambda-subscription" {
  topic_arn = aws_sns_topic.helsinki-city-bikes-object-created-notifications-topic.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.load-file-to-monthly-metrics-table-lambda.arn
}
