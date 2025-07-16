#!/bin/bash
sudo apt update -y
sudo apt install apache2 -y
sudo systemctl start apache2
sudo systemctl enable apache2

# Format and mount EBS volume
sudo mkfs -t ext4 /dev/xvdf
sudo mkdir /data
sudo mount /dev/xvdf /data
echo '/dev/xvdf /data ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab

# Add a simple portfolio page
echo "<!DOCTYPE html><html><head><title>Shivansh's Portfolio</title></head><body><h1>Hello from EC2 with EBS!</h1><p>This is a static webpage hosted on Apache via Terraform.</p></body></html>" | sudo tee /var/www/html/index.html
