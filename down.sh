#!/bin/bash

read -r -p "Please enter the experiment ID: " EXPERIMENT_ID

terraform destroy -var="KEY=0" -var="experiment_id=$EXPERIMENT_ID" -state="terraform-${EXPERIMENT_ID}.tfstate"

rm "nodes-list-${EXPERIMENT_ID}.out"
rm "terraform-${EXPERIMENT_ID}.tfstate"
rm "terraform-${EXPERIMENT_ID}.tfstate.backup"