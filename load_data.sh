#!/bin/sh

#  load_data.sh
#  
#
#  Created by Hobey Kuhn on 11/18/13.
#


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

# configure path to xml files
# NOTE: DUC PATH NOT CONFIGURED
if [ "$dataset_name" == "Australia" ]; then
    data_path="./corpus/fulltext/"
else
    echo "DUC set is unavailable at the moment!"
    break
fi

# INDEXING:
# PUT data from path onto SOLR
http://localhost:18888/solr/
