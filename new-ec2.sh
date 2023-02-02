#!/bin/bash

# Create new ec2 instance
aws ec2 run-instances \
--image-id ami-0cc814d99c59f3789 \
--count 1 \
--instance-type t3a.medium \
--key-name david-machine-key \
--security-group-id sg-02ace81231f90b040 \
--subnet-id subnet-008c16c916a651131 \
--associate-public-ip-address \
--tag-specifications 'ResourceType=instance,Tags=[{Key=Name, Value=production}, {Key=owner,Value=david-davidov}, {Key=bootcamp,Value=17}, {Key=expiration_date,Value=30-01-2023}]'