#!/bin/bash

gcloud compute firewall-rules create message-api \
  --allow=tcp:50000 \
  --target-tags=fog-computing
