#!/bin/sh

# generate_summary.sh
#
#
# Created by Hobey Kuhn on 12/05/13.
#

# Description:
#    Generates a summary with name of dataset and filename as input.

DATASET_NAME="${1}"
DOCUMENT_NAME="${2}"
DATA_DIR="../data"
AUSTRALIAN_DATASET_DIR="${DATA_DIR}/corpus/"
AUSTRALIAN_DATASET_LABELS_DIR="${DATA_DIR}/australian_dataset_labels"


# confirm dataset name and retrieve labels
if [ "${1}" = "Australia" ]; then
    dataset_labels_path="${AUSTRALIAN_DATASET_LABELS_DIR}"
else
    echo "Invalid input in command line. Please read the README to learn how to use this script!"
    exit
fi

if [ -f "${dataset_labels_path}/${DOCUMENT_NAME}" ]; then
   echo "Specified file found. Reading labels into summary generation..."
else
   echo "File specified was not found! Please make sure generate_labels.sh was run before this to ensure your labels have been generated"
fi


# parse labels into numpy lists (sentences of words)



