#!/bin/bash

# If SEDA_DEBUG_MODE is set show detailed output
if [ ! -z ${SEDA_DEBUG_MODE} ]
then
	set -ex
fi

# Get the directory of this script to use in reference to
SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )

# If given an argument output everything to there,
# if not, use EvaluationOutput in the data folder by default
if [ -z $1 ]
then
	OUTPUT_DIR="${SCRIPT_PATH}/../../data/EvaluationOutput"
else
	# Go to folder to place result output into
        OUTPUT_DIR="${SCRIPT_PATH}/../../data/${1}"
fi

# Enter directory so rouge2csv.pl leaves output there
cd "${OUTPUT_DIR}"

# Remove OUT_ROUGE-SUX.csv if it already exist,
# other wise the script would append
rm -f "OUT_ROUGE-SUX.csv"

# Convert results.out to csv format
perl "${SCRIPT_PATH}/rouge2csv.pl" "${OUTPUT_DIR}/results.out" OUT
