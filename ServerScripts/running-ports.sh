#!/bin/bash

# List all ports on which services are currently running
lsof -i -P -n | awk 'NR>1 {split($9, a, ":"); if(a[2] ~ /^[0-9]+$/) print a[2]}' | sort -n | uniq
