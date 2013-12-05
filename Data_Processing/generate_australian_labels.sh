#!/bin/sh

#  generate_australian_labels.sh
#
#
#  Created by Hobey Kuhn on 11/18/13.
#



DATASET_NAME=${1}
AUSTRALIAN_DATASET_DIR="../data/corpus/"
AUSTRALIAN_DATASET_LABELS_DIR="../data/australian_dataset_labels"


# confirm dataset name and retrieve path
if [ "${DATASET_NAME}" = "Australia" ]; then
    echo "Checking if dataset has been downloaded..."
    if [ -d "${AUSTRALIAN_DATASET_DIR}" ]; then
        echo "Dataset already exists. Skipping download..."
    else
        echo "Retrieving Dataset..."
        sh getAustralianDataset.sh
    fi 
    data_path="${AUSTRALIAN_DATASET_DIR}/fulltext/*"

else
    echo "Invalid input in command line. Please read the README to learn how to use this script!"
    exit
fi

# make directory for labels and parse files for labels
if [ "${DATASET_NAME}" = "Australia" ]; then
    echo "Retrieving labels from data..."
    mkdir "${AUSTRALIAN_DATASET_LABELS_DIR}"
    for f in ${data_path}
    do
        filename=`basename "${f}"`
        if [ "${DATASET_NAME}" = "Australia" ]; then
            echo "Retrieving Label from: ${filename}"
            python australia_xml_label_parser.py "${f}" "${AUSTRALIAN_DATASET_LABELS_DIR}/${filename}"
        fi
    done
fi

