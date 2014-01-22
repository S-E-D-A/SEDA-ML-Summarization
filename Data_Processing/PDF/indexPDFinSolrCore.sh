#!/bin/bash

###
### This script takes a text file and indexes it as a document in Solr
### -c The core name that this is indexed to
### -p The path of the file with the text
###

# If SEDA_DEBUG_MODE is set show detailed output
if [ ! -z ${SEDA_DEBUG_MODE} ]
then
        set -ex
fi

# Variable of whether or not to Recreate core
CREATE_CORE=0

# The function to describe how to run the script
USAGE_STRING="Usage: $0 [-c <core_name>] [-p <path_to_file>] [-n create core ][-h help]"
usage() { echo ${USAGE_STRING} 1>&2; exit 1; }

while getopts ":c:p:nh" o; do
    case "${o}" in
        c)
            CORE_NAME=${OPTARG}
            ;;
        p)
            PATH_TO_FILE=${OPTARG}
            ;;
	n)
	    CREATE_CORE=1
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

if [ -z "${CORE_NAME}" ] || [ -z "${PATH_TO_FILE}" ]; then
    usage
fi

# Get the directory of this script to use in reference to
SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )

SOLR_BASE="http://localhost:8983/solr"

if [ ${CREATE_CORE} -eq 1 ]; then
	# Delete the index if it already exists
	curl "${SOLR_BASE}/admin/cores?action=UNLOAD&core=${CORE_NAME}&deleteInstanceDir=true"

	# Remove the core if it already exists
	rm -rf "/home/${USER}/${CORE_NAME}"

	# Copy new instanceDir over for this core
	cp -af "${SCRIPT_PATH}/../solr_config" "/home/${USER}/${CORE_NAME}"

	# Build core
	echo "Building new SOLR core..."
	curl "${SOLR_BASE}/admin/cores?action=CREATE&name=${CORE_NAME}&instanceDir=/home/vagrant/${CORE_NAME}/collection1"
fi

# post files to core
#java -Durl="${SOLR_BASE}/${1}/update" -jar "${SCRIPT_PATH}/../post.jar" "${2}"
curl "${SOLR_BASE}/${CORE_NAME}/update/extract?stream.file=`readlink -f ${PATH_TO_FILE}`&stream.contentType=application/pdf&literal.id=`basename ${PATH_TO_FILE}`"

# Run optimize core so the core  information is up to date
curl "${SOLR_BASE}/${CORE_NAME}/update?optimize=true"
