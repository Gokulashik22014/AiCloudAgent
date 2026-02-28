provider "aws" {
  region = var.region
}

# Fetch latest Amazon Linux 2 AMI automatically
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

resource "aws_instance" "basic" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
  count = var.instance_count
  tags = {
    Name = var.instance_name
    ManagedBy = "AgentSystem"
  }
}
