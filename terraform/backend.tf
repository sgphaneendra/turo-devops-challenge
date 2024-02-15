terraform {
  backend "s3" {
    bucket = "terraform-tfstate-sai"
    key    = "terraform/state"
    region = "us-east-1"
  }
}
provider "aws" {
  region = "us-east-1"
}
