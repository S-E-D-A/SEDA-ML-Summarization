#!/bin/bash

###
### This script takes a PDF file and converts it into a text document
### arg1: input file path
### arg2: output file path
###

# If SEDA_DEBUG_MODE is set show detailed output
if [ ! -z ${SEDA_DEBUG_MODE} ]
then
        set -ex
fi

# The function to describe how to run the script
USAGE_STRING="Usage: $0 [-i <input_pdf_file>] [-o <output_text_file>] [-h help]"
usage() { echo ${USAGE_STRING} 1>&2; exit 1; }

while getopts ":i:o:h" o; do
    case "${o}" in
        i)
            INPUT_FILE=${OPTARG}
            ;;
        o)
            OUTPUT_FILE=${OPTARG}
            ;;
        h)
            usage
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${INPUT_FILE}" ] || [ -z "${OUTPUT_FILE}" ]; then
    usage
fi

# Get the directory of this script to use in reference to
SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )

# Perform the conversion from PDF to text
java -jar "${SCRIPT_PATH}/pdfbox-app-1.8.3.jar" ExtractText -nonSeq "${INPUT_FILE}" "${OUTPUT_FILE}"
