#!/bin/bash

# Get the directory of this script to use in reference to
SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )

ROUGE_FILE_NAME="ROUGE-1.5.5.tgz"
ROUGE_URL="https://www.dropbox.com/s/plcw48pi0rjzkge/${ROUGE_FILE_NAME}"
DOT_ROUGE_INSTALLED="${SCRIPT_PATH}/.rougeinstalled"

# Install necessary Perl package for Rouge to functin
perl -MCPAN -e 'force install XML::DOM'

if [ ! -f "${DOT_ROUGE_INSTALLED}" ]; then
	echo "Installing ROUGE.\n"

	# Download Rouge
	wget "${ROUGE_URL}" -O "${SCRIPT_PATH}/${ROUGE_FILE_NAME}"

	# Unzip Rouge
	tar -zxvf "${SCRIPT_PATH}/${ROUGE_FILE_NAME}" \
		--directory="${SCRIPT_PATH}"

	# Remove the tar file
	rm "${SCRIPT_PATH}/${ROUGE_FILE_NAME}"

	# Create file to indicate the file has been installed
	touch "${DOT_ROUGE_INSTALLED}"
else
	echo "Rouge installed.\n"
fi
