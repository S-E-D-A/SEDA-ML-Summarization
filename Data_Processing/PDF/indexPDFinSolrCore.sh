#!/bin/bash

###
### This script takes a text file and indexes it as a document in Solr
### arg1: The core name that this is indexed to
### arg2: The path of the file with the text
###

# If SEDA_DEBUG_MODE is set show detailed output
if [ ! -z ${SEDA_DEBUG_MODE} ]
then
        set -ex
fi

# Check if there are 2 arguments, one for core name, other for text file
if [ $# -ne 2 ]; then
  echo "#############################################"
  echo "Error, incorrect number of arguments supplied"
  echo "Usage: $0 NEW_CORE_NAME path/to/file"
  exit
fi

# Get the directory of this script to use in reference to
SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )

SOLR_BASE="http://localhost:8983/solr"

# Delete the index if it already exists
curl "${SOLR_BASE}/admin/cores?action=UNLOAD&core=${1}&deleteInstanceDir=true"

# Remove the core if it already exists
rm -rf "/home/${USER}/${1}"

# Copy new instanceDir over for this core
cp -af "${SCRIPT_PATH}/../solr_config" "/home/${USER}/${1}"

# Build core
echo "Building new SOLR core..."
curl "${SOLR_BASE}/admin/cores?action=CREATE&name=${1}&instanceDir=/home/vagrant/${1}/collection1"

# post files to core
#java -Durl="${SOLR_BASE}/${1}/update" -jar "${SCRIPT_PATH}/../post.jar" "${2}"
curl "${SOLR_BASE}/${1}/update/extract?stream.file=`readlink -f ${2}`&stream.contentType=application/pdf&literal.id=${1}"
