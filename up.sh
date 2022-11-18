#!/bin/sh

KEY=$(cat .key)
HYDRA_IGNORE_PCT=$(cat .ignored_heads_pct)
terraform apply -var="KEY=$KEY" -var="HYDRA_IGNORE_PCT=$HYDRA_IGNORE_PCT" -state=terraform-wo-${HYDRA_IGNORE_PCT}pct.tfstate
sleep 5
terraform output > nodes-list-wo-${HYDRA_IGNORE_PCT}pct.out
monitorIP=$(head -1 ./nodes-list-wo-${HYDRA_IGNORE_PCT}pct.out | cut -d'"' -f2)
echo "monitor URL is $monitorIP:3000"
open "http://$monitorIP:3000"