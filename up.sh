#!/bin/sh

read -r -p "Please enter the experiment ID: " EXPERIMENT_ID

KEY=$(cat .key)
terraform apply -var="KEY=$KEY" -var="experiment_id=$EXPERIMENT_ID" -state="terraform-${EXPERIMENT_ID}.tfstate"
sleep 5
terraform output -state="terraform-${EXPERIMENT_ID}.tfstate" > "nodes-list-${EXPERIMENT_ID}.out"
monitorIP=$(head -1 "nodes-list-${EXPERIMENT_ID}.out" | cut -d'"' -f2)
echo "monitor URL is $monitorIP:3000"
open "http://$monitorIP:3000"