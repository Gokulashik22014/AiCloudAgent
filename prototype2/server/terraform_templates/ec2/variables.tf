variable "region" {
  description = "AWS region to deploy"
  type        = string
  default     = "ap-south-1"

  validation {
    condition     = contains(["ap-south-1", "us-east-1", "us-west-2"], var.region)
    error_message = "Region must be one of: ap-south-1, us-east-1, us-west-2."
  }
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
  validation {
    condition = contains(["t2.micro","t3.micro"],var.instance_type)
    error_message = "Instance Type must be of: T2 or T3 micro"
  }
}

variable "ami" {
  description = "AMI ID for the instance"
  type        = string
  default     = "ami-053b0d53c279acc90" # Amazon Linux (example for ap-south-1)
}

variable "instance_name" {
  description = "Name tag for EC2"
  type        = string
  default     = "terraform-ec2"
}