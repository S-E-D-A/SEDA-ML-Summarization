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

# Check if there are 2 arguments, one for core name, other for text file
# Optional check for field name as argument
if [ $# -lt 2 ] || [ $# -gt 3 ]; then
  echo "#############################################"
  echo "Error, incorrect number of arguments supplied"
  echo "Usage: $0 CORE_NAME PATH_AND_OUTPUT_NAME OPTIONAL_field_name"
  exit
fi

TERM_VECTOR_FIELD="content"
# Optional argument of field name, set if it exists
if [ ! -z ${3} ]; then
  TERM_VECTOR_FIELD="${3}"
fi

BASE_URL="http://localhost:8983/solr"
CORE="${1}"
QUERY="tvrh?q=*%3A*&wt=python&indent=true&tv.fl=${TERM_VECTOR_FIELD}&tv.all=true&fl=false&start=0&rows=999999999"
FINAL_QUERY="${BASE_URL}/${CORE}/${QUERY}"

echo ${FINAL_QUERY}
echo "Writing ${1} dataset term frequencies to ${2}" 

curl "${FINAL_QUERY}" > "${2}"
