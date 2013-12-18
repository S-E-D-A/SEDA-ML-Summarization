#!/bin/bash

# If SEDA_DEBUG_MODe is set show detailed output
if [ ! -z ${SEDA_DEBUG_MODE} ]
then
	set -ex
fi

# Get the directory of this script to use in reference to
SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )

# Install ROUGE
sh "${SCRIPT_PATH}/ROUGE/installRouge.sh"

# Store ROGUE installation directory in variable
ROUGE_DIRECTORY="${SCRIPT_PATH}/ROUGE/RELEASE-1.5.5"

# Set variable for ROUGE executable
ROUGE="${ROUGE_DIRECTORY}/ROUGE-1.5.5.pl"

# Stroe the generate.py script into a variable
GENERATE_PY="${SCRIPT_PATH}/generation_scripts/generate.py"

# If given an argument output everything to there,
# if not, use EvaluationOutput in the data folder by default
if [ -z $1 ]
then
	eval "${GENERATE_PY}" 
	OUTPUT_DIR="${SCRIPT_PATH}/../data/EvaluationOutput"
else
	eval "${GENERATE_PY}" "${1}"
	OUTPUT_DIR="${SCRIPT_PATH}/../data/${1}"
fi

# Generate ROUGE results
eval "${ROUGE}" -e "${ROUGE_DIRECTORY}/data" \
	-f A -a -x -s -m -2 -4 -u "${OUTPUT_DIR}/rougeFiles/settings.xml" > \
	"${OUTPUT_DIR}/results.out"

# Convert the ROUGE generated results to a csv format
if [ -z $1 ]
then
	sh "${SCRIPT_PATH}/generation_scripts/convertResults.sh" 
else
	sh "${SCRIPT_PATH}/generation_scripts/convertResults.sh" ${1}
fi
