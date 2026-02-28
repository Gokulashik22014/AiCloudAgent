variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "instance_name" {
  description = "Name tag for EC2"
  type        = string
}

variable "instance_count" {
  default = 1
  type = number
  description = "Specify the number of instances"
}