#!/bin/bash

##
## This script downloads and unzips the Australian Legal Dataset into ../data if it is not already present.
##

DATASET_ZIP_FILE="corpus.zip"
DATASET_URL="https://www.dropbox.com/s/qspwwkktycacyyj/${DATASET_ZIP_FILE}"
DATASET_DIRECTORY="../data"
CORPUS_DIRECTORY="${DATASET_DIRECTORY}/corpus"

# Download and unzip only if it's not present
if [ ! -d "${CORPUS_DIRECTORY}" ]; then
  # Download corpus.zip into data directory
  wget "${DATASET_URL}" -O "${DATASET_DIRECTORY}/${DATASET_ZIP_FILE}"

  # Unzip corpus.zip in data folder
  unzip "${DATASET_DIRECTORY}/${DATASET_ZIP_FILE}" -d "${DATASET_DIRECTORY}"
  
  # Remove the compressed file
  rm "${DATASET_DIRECTORY}/${DATASET_ZIP_FILE}"

  echo "Downloaded and unzipped ${DATASET_ZIP_FILE} in ${CORPUS_DIRECTORY}"
else
  # Nothing needs to be done if /.solrinstalled is present
  echo "Corpus already unzipped."
fi
