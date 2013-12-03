#!/bin/sh

#  load_data.sh
#  
#
#  Created by Hobey Kuhn on 11/18/13.
#





# configure path to json files
# NOTE: DUC PATH NOT CONFIGURED
if [ ${1} = "Australia" ]; then
    # Obtains and unzips the Australian dataset if not alraedy present
    sh getAustralianDataset.sh
    data_path="./corpus/fulltext/*"

else
    echo "Invalid input in command line. Please read the README to learn how to use this script!"
    exit
fi

# INDEXING:
# Parse XML for SOLR Format
if [ -d "solr_files" ]; then
    echo "skipping conversion..."
else
    mkdir "solr_files"
    echo "Converting files into a format compatible with SOLR"
    for f in ${data_path}
    do
        filename=$(basename $f)
    if [ "${1}" = "Australia" ]; then
        python australia_xml_parser.py "${f}" "solr_files/${filename}"
    fi
    done
fi
# PUT data from path onto SOLR
echo "Posting files to SOLR"
cp -a "solr_config" "/home/vagrant"
curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=${2}&instanceDir=/home/vagrant/solr_config/collection1"
java -Durl=http://localhost:8983/solr/${2}/update -jar post.jar "solr_files/*.xml"
