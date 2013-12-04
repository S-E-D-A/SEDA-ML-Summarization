BASE_URL="http://localhost:8983/solr"
CORE="AustralianDataset"
QUERY="tvrh?q=*%3A*&wt=python&indent=true&tv.fl=features&tv.all=true&fl=false&start=0&rows=999999999"
FINAL_QUERY="${BASE_URL}/${CORE}/${QUERY}"

echo ${FINAL_QUERY}
echo "Writing Ausralian legal dataset term frequencies" 

# Get the directory of this script to use in reference to
SCRIPT_PATH=$( cd $(dirname $0) ; pwd -P )
DATASET_DIRECTORY="${SCRIPT_PATH}/../data"

curl "${FINAL_QUERY}" > "${DATASET_DIRECTORY}/australianLegalDataset_term_frequencies"
