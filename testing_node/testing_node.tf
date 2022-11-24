terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.33.0"
    }
  }
}

variable "monitoring_ip" {
  type = string
}

variable "key" {
  type = string
}

variable "experiment_id" {
  type = string
}

variable "ssh_key" {
  type = string
}

variable "ami" {
  type = string
}

variable "num" {
  type = string
}

variable "default_tags" {
  type = map(any)
}

variable "instance" {
  type    = string
  default = "t3.xlarge"
}

output "public_ip" {
  value = aws_instance.ipfs_testing_node.public_ip
}

resource "aws_instance" "ipfs_testing_node" {
  ami             = var.ami
  instance_type   = var.instance
  key_name        = aws_key_pair.ssh_key.key_name
  security_groups = [aws_security_group.security_ipfs_testing_node.name]

  user_data = <<-EOF
    #!/bin/sh
    cd /home/ubuntu/
    sudo apt-get update
    sudo apt install -y unzip git make build-essential jq
    wget https://github.com/grafana/loki/releases/download/v2.3.0/promtail-linux-amd64.zip
    wget https://golang.org/dl/go1.18.1.linux-amd64.tar.gz
    wget https://raw.githubusercontent.com/dennis-tra/ipfs-lookup-measurement/main/node/promtail-cloud-config.yaml
    unzip ./promtail-linux-amd64.zip
    sudo tar -C /usr/local -xzf go1.18.1.linux-amd64.tar.gz
    mkdir /home/ubuntu/go
    export HOME=/home/ubuntu
    export GOPATH=/home/ubuntu/go
    export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
    git clone https://github.com/dennis-tra/ipfs-lookup-measurement.git
    cd ipfs-lookup-measurement
    git checkout main
    cd controller
    make agent
    cd ..
    cd ..
    git clone https://github.com/dennis-tra/go-libp2p-kad-dht.git
    cd go-libp2p-kad-dht
    git checkout v0.18.0-more-logging
    cd ..
    git clone https://github.com/dennis-tra/go-bitswap.git
    cd go-bitswap
    git checkout v0.10.2-more-logging
    cd ..
    git clone https://github.com/dennis-tra/go-ipfs.git
    cd go-ipfs
    git checkout v0.17.0-more-logging
    echo "replace github.com/libp2p/go-libp2p-kad-dht => ../go-libp2p-kad-dht" >> go.mod
    echo "replace github.com/ipfs/go-bitswap => ../go-bitswap" >> go.mod
    go mod tidy
    make build > buildLog.txt 2>&1
    cd ..
    mkdir ./ipfs-tests/
    export KEY="${var.key}"
    export IP="${var.monitoring_ip}"
    export PERFORMANCE_TEST_DIR=/home/ubuntu/ipfs-tests/
    export IPFS_PATH=/home/ubuntu/.ipfs
    export IPFS=/home/ubuntu/go-ipfs/cmd/ipfs/ipfs
    echo "$KEY" > ./ipfs-tests/.key
    echo "      host: node${var.num}" >> ./promtail-cloud-config.yaml
    echo "clients:" >> ./promtail-cloud-config.yaml
    echo "  - url: http://$IP:3100/loki/api/v1/push" >> ./promtail-cloud-config.yaml
    nohup ./promtail-linux-amd64 -config.file=promtail-cloud-config.yaml &
    ./go-ipfs/cmd/ipfs/ipfs init
    cat ./.ipfs/config | jq '.Swarm.ResourceMgr.Enabled=false' > ./.ipfs/config-new
    rm ./.ipfs/config
    mv ./.ipfs/config-new ./.ipfs/config
    nohup ./go-ipfs/cmd/ipfs/ipfs daemon > /home/ubuntu/all.log 2>&1 &
    IPFS_LOGGING=INFO nohup ./ipfs-lookup-measurement/controller/agent > /home/ubuntu/agent.log 2>&1 &
  EOF

  tags = merge(var.default_tags, {
    Name = "ipfs-testing-node-${var.experiment_id}-${var.num}"
  })
}

resource "aws_security_group" "security_ipfs_testing_node" {
  name        = "security_ipfs_testing_node_${var.experiment_id}-${var.num}"
  description = "security group for ipfs testing node"

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
    from_port   = 4001
    to_port     = 4001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 4001
    to_port     = 4001
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3030
    to_port     = 3030
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.default_tags, {
    Name = "security_ipfs_testing_node_${var.experiment_id}-${var.num}"
  })
}

resource "aws_key_pair" "ssh_key" {
  key_name   = "ssh-key-node-${var.experiment_id}"
  public_key = var.ssh_key
}