#!/bin/bash

##
## This script downloads and unzips the Australian Legal Dataset if it is not already present
##

DATASET_ZIP_FILE="corpus.zip"
DATASET_URL="http://archive.ics.uci.edu/ml/machine-learning-databases/00239/${DATASET_ZIP_FILE}"
DATASET_DIRECTORY="corpus"

# Download and unzip only if it's not present
if [ ! -d corpus ]; then
  # Download
  curl -O ${DATASET_URL}
  # Unzip
  unzip ${DATASET_ZIP_FILE}
  # Remove the compressed file
  rm ${DATASET_ZIP_FILE}

  echo "Downloaded and unzipped corpus.zip"
else
  # Nothing needs to be done if /.solrinstalled is present
  echo "Corpus already unzipped."
fi
