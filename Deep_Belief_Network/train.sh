#!/bin/bash

# If SEDA_DEBUG_MODE is set show detailed output
if [ ! -z ${SEDA_DEBUG_MODE} ]
then
  set -ex
fi

# The function to describe how to run the script
USAGE_STRING="Usage: $0 [-p <path_to_file>] [-n <number_of_documents>] [-h help]"
usage() { echo ${USAGE_STRING} 1>&2; exit 1; }

while getopts ":p:n:h" o; do
    case "${o}" in
        p)
            PATH_TO_FILE=${OPTARG}
            ;;
        n)
            NUM_DOCS=${OPTARG}
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

if [ -z "${PATH_TO_FILE}" ] || [ -z "${NUM_DOCS}" ]; then
    usage
fi

python train_RBM_DBN.py -p ${PATH_TO_FILE} -n ${NUM_DOCS}
