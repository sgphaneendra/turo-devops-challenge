variable "deployment_yaml" {
  type        = string
  description = "Kubernetes Deploy Manifest"
}

variable "image_name" {
  type        = string
  description = "The image to be deployed"
}

variable "kube_namespace" {
  type        = string
  description = "Kube namespace to create and deploy app to"
}

variable "ssl_service_yaml" {
  type        = string
  description = "Kubernetes SSL Service Manifest"
}

variable "configmap_yaml" {
  type        = string
  description = "Kubernetes Configmap Manifest"
}

variable "ingress_yaml" {
  type        = string
  description = "Kubernetes ingress Manifest"
}

variable "acm_arn" {
  type        = string
  description = "AWS ACM arn value for SSL service"
}

variable "dns_name" {
  type        = string
  description = "Value of dns domain name"
}