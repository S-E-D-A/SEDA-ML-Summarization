#!/bin/sh

# generate_summary.sh
#
#
# Created by Hobey Kuhn on 12/05/13.
#

# Description:
#    Generates a summary with name of dataset and filename as input.
#
# Example:
#    sh generate_summary.sh Australia 07_222.xml query 2 200


DATASET_NAME="${1}"
DOCUMENT_NAME="${2}"
QUERY_NAME="${3}"
LAMBDA="${4}"
MAX_WORDS="${5}"


DATA_DIR="../data"

SOLR_DATA_DIR="${DATA_DIR}/solr_xml_files"

AUSTRALIAN_DATASET_DIR="${DATA_DIR}/corpus/"
AUSTRALIAN_DATASET_LABELS_DIR="${DATA_DIR}/australian_dataset_labels"




# confirm dataset name and retrieve labels
if [ "${DATASET_NAME}" = "Australia" ]; then
    dataset_labels_path="${AUSTRALIAN_DATASET_LABELS_DIR}"
    dataset_core_name="AustralianDataset"
    dataset_path="${AUSTRALIAN_DATASET_DIR}/fulltext/"
else
    echo "Invalid input in command line. Please read the README to learn how to use this script!"
    exit
fi

# Test if labels have been generated
if [ -f "${dataset_labels_path}/${DOCUMENT_NAME}" ]; then
   echo "Specified file found. Continuing..."
else
   echo "File specified was not found! Please make sure generate_labels.sh was run before this to ensure your labels have been generated"
   exit
fi


# generate vocabulary for summary generation
#    first, run query to obtain vocabulary
#    then, run build_vocabulary.py to create numpy file
if [ -f "dictionary" ]; then
    echo "Dictionary data already exists. Skipping query from SOLR to retrieve dictionary data..."
else
    echo "Retrieving dictionary from SOLR..."
    curl "http://localhost:8983/solr/${dataset_core_name}/terms?wt=python&indent=true&terms.fl=features&terms.limit=-1" > "dictionary"
    echo "Parsing vocabulary dictionary into pickled file called fD_pickled"
fi

python parse_vocabulary_into_list.py dictionary
echo "cleaning up"
#rm dictionary



# retrieve sentences from input document
if [ -f "${2%.*}_sentences_array" ]; then
    echo "Document specified has already been parsed into a pickled file. Skipping..."
else
    echo "Pickling input file..."
    python parse_document_into_sentences.py "${SOLR_DATA_DIR}/${DOCUMENT_NAME}"
fi


# Run summary generation with input files to create a summary
python run_summary_generation.py ../data/vocabulary_list.npy fD_pickled "${2%.*}_sentences_array" "${QUERY}" "${LAMBDA}" "${MAX_WORDS}"


# Print summary
python print_summary.py

# CLEANUP
echo "\n\n\n"
echo "Cleaning up..."


 
