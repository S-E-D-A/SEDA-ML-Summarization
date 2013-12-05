#!/bin/sh

# generate_summary.sh
#
#
# Created by Hobey Kuhn on 12/05/13.
#


DATASET_NAME="${1}"
DATA_DIR="../data"
DATA_PROCESSING_DIR="../Data_Processing"
AUSTRALIAN_DATASET_DIR="${DATA_DIR}/corpus/"
AUSTRALIAN_DATASET_LABELS_DIR="${DATA_DIR}/australian_dataset_labels"


# confirm dataset name and retrieve labels
if [ "${DATASET_NAME}" = "Australia" ]; then
    echo "Retrieving labels.."
    sh "${DATA_PROCESSING_DIR}/generate_australian_labels.sh" Australia

else
    echo "Invalid input in command line. Please read the README to learn how to use this script!"
    exit
fi




