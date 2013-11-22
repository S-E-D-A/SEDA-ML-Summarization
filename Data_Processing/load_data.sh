#!/bin/sh

#  load_data.sh
#  
#
#  Created by Hobey Kuhn on 11/18/13.
#



# Enforce JSON format
echo "Before continuing, make sure your files in xml format! Also make sure that there is no directory called solr_files if you are planning on converting files first"

# read in file name
echo "Which dataset do you wish to load? Specify: Australia / DUC"
read dataset_name


# test input
flag=true
while [ $flag ]; do
    if [ "$dataset_name" != "Australia" ] && [ "$dataset_name" != "DUC" ]; then
        echo "Please enter either Australia or DUC"
        read dataset_name
    else
        break
    fi
done

# configure path to json files
# NOTE: DUC PATH NOT CONFIGURED
if [ "$dataset_name" == "Australia" ]; then
    data_path="corpus/fulltext/*"

else
    echo "DUC set is unavailable at the moment!"
    break
fi

# INDEXING:
# Parse XML for SOLR Format
if [ -d "solr_files" ]; then
    echo "skipping conversion..."
else
    mkdir "solr_files"
    echo "Converting files into a format compatible with SOLR"
    for f in $data_path
    do
        filename=$(basename $f)
    if [ "$dataset_name" == "Australia" ]; then
        python australia_xml_parser.py "$f" "solr_files/$filename"
    fi
    done
fi
# PUT data from path onto SOLR
echo "Posting files to SOLR"
java -Durl=http://localhost:18983/solr/update -jar post.jar "solr_files/*.xml"
