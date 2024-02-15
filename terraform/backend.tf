terraform {
  backend "s3" {
    bucket = "terraform-tfstate-sai"
    key    = "terraform/state"
    region = "eu-west-2"
  }
}
provider "aws" {
  region = "eu-west-2"
}
