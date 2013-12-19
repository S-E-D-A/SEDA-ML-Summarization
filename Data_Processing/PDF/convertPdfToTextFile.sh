#!/bin/bash

# If SEDA_DEBUG_MODE is set show detailed output
if [ ! -z ${SEDA_DEBUG_MODE} ]
then
        set -ex
fi

# Check if there are 2 arguments, one for core name, other for text file
if [ $# -ne 2 ]; then
  echo "#############################################"
  echo "Error, incorrect number of arguments supplied"
  echo "Usage: $0 INPUT_PDF_PATH OUTPUT_PATH_NAME"
  exit
fi

# Get the directory of this script to use in reference to
SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )

java -jar "${SCRIPT_PATH}/pdfbox-app-1.8.3.jar" ExtractText -nonSeq $1 $2
