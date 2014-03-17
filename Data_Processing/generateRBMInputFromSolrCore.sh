#!/bin/bash

### 
### This script takes any CORE_NAME and stores the term frequency into the second argument
### arg1: name of solr core to retrieve tf values from (must have termvectors on)
### arg2: path and name of file to output to
### arg3: optional, the field name for which to retrieve termvectors
###

# If SEDA_DEBUG_MODE is set show detailed output
if [ ! -z ${SEDA_DEBUG_MODE} ]
then
  set -ex
fi

# The function to describe how to run the script
USAGE_STRING="Usage: $0 [-c <core_name>] [-p <output_path_and_file>] [-f OPTIONAL_field_name ][-h help]"
usage() { echo ${USAGE_STRING} 1>&2; exit 1; }

while getopts ":c:p:f:h" o; do
    case "${o}" in
        c)
            CORE_NAME=${OPTARG}
            ;;
        p)
            PATH_TO_FILE=${OPTARG}
            ;;
        f)
            FIELD_NAME=${OPTARG}
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

if [ -z "${PATH_TO_FILE}" ] || [ -z "${CORE_NAME}" ]; then
    usage
fi

TERM_VECTOR_FIELD="content"
# Optional argument of field name, set if it exists
if [ ! -z ${FIELD_NAME} ]; then
  TERM_VECTOR_FIELD="${FIELD_NAME}"
fi

BASE_URL="http://localhost:8983/solr"
CORE="${CORE_NAME}"
QUERY="tvrh?q=*%3A*&wt=python&indent=true&tv.fl=${TERM_VECTOR_FIELD}&tv.all=true&fl=false&start=0&rows=999999999"
FINAL_QUERY="${BASE_URL}/${CORE}/${QUERY}"

echo ${FINAL_QUERY}
echo "Writing ${CORE_NAME} dataset term frequencies to ${PATH_TO_FILE}" 

curl "${FINAL_QUERY}" > "${PATH_TO_FILE}"
