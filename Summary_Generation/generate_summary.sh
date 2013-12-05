#!/bin/sh

# generate_summary.sh
#
#
# Created by Hobey Kuhn on 12/05/13.
#


DATASET_NAME="${1}"
DATA_DIR="../data"
AUSTRALIAN_DATASET_DIR="${DATA_DIR}/corpus/"
AUSTRALIAN_DATASET_LABELS_DIR="${DATA_DIR}/australian_dataset_labels"


# confirm dataset name and retrieve labels
echo "Retrieving labels.."
sh generate_labels.sh "${DATASET_NAME}"


# parse labels into numpy lists (sentences of words)



