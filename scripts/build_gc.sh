#!/bin/bash

# Create SSH key
KEY_NAME="id_rsa"
CONFIG_NAME="key_config"
USER_NAME="foggy"
ssh-keygen -b 2048 -t rsa -f $KEY_NAME -q -N "" -C $USER_NAME
# Prepare GCP metadata format
echo -n $USER_NAME > $CONFIG_NAME
echo -n ":" >> $CONFIG_NAME
cat $KEY_NAME.pub >> $CONFIG_NAME

# Upload SSH key
gcloud compute project-info add-metadata \
  --metadata-from-file=ssh-keys=$CONFIG_NAME

# create firewall
gcloud compute firewall-rules create message-api \
  --allow=tcp:50000 \
  --target-tags=fog-computing

# create instance
gcloud compute instances create fog-instance-1 \
  --zone "europe-west3-a" \
  --image-family "cos-stable" \
  --image-project "cos-cloud" \
  --tags "fog-computing" \
  --machine-type "e2-standard-2" \

# Extract IP address of the running machine
IP=$(gcloud compute instances describe fog-instance-1 \
  --zone=europe-west3-a \
  --format='get(networkInterfaces[0].accessConfigs[0].natIP)' \
  )

echo $IP