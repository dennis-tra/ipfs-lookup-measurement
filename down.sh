#!/bin/bash

HYDRA_IGNORE_PCT=$(cat .ignored_heads_pct)
terraform destroy -var="KEY=0" -var="HYDRA_IGNORE_PCT=$HYDRA_IGNORE_PCT" -state=terraform-wo-${HYDRA_IGNORE_PCT}pct.tfstate