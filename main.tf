terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.33.0"
    }
  }
  required_version = ">= 1.0"
}

variable "KEY" {
  type = string
}

variable "experiment_id" {
  type = string
}

provider "aws" {
  # Bahrain
  # AMI: ami-0b4946d7420c44be4
  region = "me-south-1"
  alias  = "me_south_1"
}

provider "aws" {
  # Sydney
  # AMI: ami-0bf8b986de7e3c7ce
  region = "ap-southeast-2"
  alias  = "ap_southeast_2"
}

provider "aws" {
  # Cape Town
  # AMI: ami-0ff86122fd4ad7208
  region = "af-south-1"
  alias  = "af_south_1"
}

provider "aws" {
  # N. California
  # AMI: ami-053ac55bdcfe96e85
  region = "us-west-1"
  alias  = "us_west_1"
}

provider "aws" {
  # Frankfurt
  # AMI: ami-0a49b025fffbbdac6
  region = "eu-central-1"
  alias  = "eu_central_1"
}

provider "aws" {
  # Sao Paulo
  # AMI: ami-0e66f5495b4efdd0f
  region = "sa-east-1"
  alias  = "sa_east_1"
}

locals {
  default_tags = {
    Terraformed = true
    Project     = "protocol-labs-dht-measurement"
  }
}

module "testing_node_0" {
  source = "./testing_node"

  monitoring_ip = aws_instance.ipfs_testing_monitor.public_ip
  key           = var.KEY
  experiment_id = var.experiment_id
  ami           = "ami-0b4946d7420c44be4"
  instance      = "t3.small"
  num           = 0
  default_tags  = local.default_tags

  providers = {
    aws = aws.me_south_1
  }
}

module "testing_node_1" {
  source = "./testing_node"

  monitoring_ip = aws_instance.ipfs_testing_monitor.public_ip
  key           = var.KEY
  experiment_id = var.experiment_id
  ami           = "ami-0bf8b986de7e3c7ce"
  num           = 1
  default_tags  = local.default_tags

  providers = {
    aws = aws.ap_southeast_2
  }
}

module "testing_node_2" {
  source = "./testing_node"

  monitoring_ip = aws_instance.ipfs_testing_monitor.public_ip
  key           = var.KEY
  experiment_id = var.experiment_id
  ami           = "ami-0ff86122fd4ad7208"
  instance      = "t3.small"
  num           = 2
  default_tags  = local.default_tags

  providers = {
    aws = aws.af_south_1
  }
}

module "testing_node_3" {
  source = "./testing_node"

  monitoring_ip = aws_instance.ipfs_testing_monitor.public_ip
  key           = var.KEY
  experiment_id = var.experiment_id
  ami           = "ami-053ac55bdcfe96e85"
  num           = 3
  default_tags  = local.default_tags

  providers = {
    aws = aws.us_west_1
  }
}

module "testing_node_4" {
  source = "./testing_node"

  monitoring_ip = aws_instance.ipfs_testing_monitor.public_ip
  key           = var.KEY
  experiment_id = var.experiment_id
  ami           = "ami-0a49b025fffbbdac6"
  num           = 4
  default_tags  = local.default_tags

  providers = {
    aws = aws.eu_central_1
  }
}

module "testing_node_5" {
  source = "./testing_node"

  monitoring_ip = aws_instance.ipfs_testing_monitor.public_ip
  key           = var.KEY
  experiment_id = var.experiment_id
  ami           = "ami-0e66f5495b4efdd0f"
  num           = 5
  default_tags  = local.default_tags

  providers = {
    aws = aws.sa_east_1
  }
}

resource "aws_instance" "ipfs_testing_monitor" {
  ami           = "ami-0a49b025fffbbdac6"
  provider      = aws.eu_central_1
  instance_type = "t2.small"

  security_groups = [aws_security_group.security_ipfs_testing_monitor.name]
  user_data       = <<-EOF
    #!/bin/sh
    cd /home/ubuntu/
    sudo apt-get update
    sudo apt install -y unzip make wget
    wget https://github.com/grafana/loki/releases/download/v2.3.0/loki-linux-amd64.zip
    wget https://dl.grafana.com/oss/release/grafana-8.1.5.linux-amd64.tar.gz
    wget https://raw.githubusercontent.com/grafana/loki/v2.3.0/cmd/loki/loki-local-config.yaml
    wget https://raw.githubusercontent.com/ConsenSys/ipfs-lookup-measurement/main/monitor/grafana-datasources.yml
    wget https://raw.githubusercontent.com/ConsenSys/ipfs-lookup-measurement/main/monitor/grafana-dashboards.yml
    wget https://raw.githubusercontent.com/ConsenSys/ipfs-lookup-measurement/main/monitor/ipfs-dashboard.json
    unzip loki-linux-amd64.zip
    tar -zxvf grafana-8.1.5.linux-amd64.tar.gz
    mv grafana-datasources.yml ./grafana-8.1.5/conf/provisioning/datasources/datasources.yml
    mv grafana-dashboards.yml ./grafana-8.1.5/conf/provisioning/dashboards/dashboards.yml
    sudo mkdir --parents /var/lib/grafana/dashboards
    mv ipfs-dashboard.json /var/lib/grafana/dashboards/
    nohup ./loki-linux-amd64 -config.file=loki-local-config.yaml &
    cd ./grafana-8.1.5/bin
    nohup ./grafana-server &

    # install Go
    cd /home/ubuntu/
    wget https://go.dev/dl/go1.19.3.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go1.19.3.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    echo 'export PATH=$PATH:/usr/local/go/bin' >> .bashrc

    # install controller
    git clone https://github.com/dennis-tra/ipfs-lookup-measurement.git
    echo "${var.KEY}" > ./ipfs-lookup-measurement/.key

    chown ubuntu:ubuntu -R ipfs-lookup-measurement
    cd ipfs-lookup-measurement/controller
    make controller
  EOF

  tags = merge(local.default_tags, {
    Name = "ipfs_testing_monitor_${var.experiment_id}"
  })
}

resource "aws_security_group" "security_ipfs_testing_monitor" {
  name        = "security_ipfs_testing_monitor_${var.experiment_id}"
  description = "security group for ipfs testing monitor"
  provider    = aws.eu_central_1

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3100
    to_port     = 3100
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.default_tags, {
    Name = "security_ipfs_testing_monitor_${var.experiment_id}"
  })
}
