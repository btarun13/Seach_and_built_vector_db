#!/usr/bin/env bash

Link="http://www.ncbi.nlm.nih.gov/pubmed/"
PMCLink="http://www.ncbi.nlm.nih.gov/pmc/articles/"

# Check if at least one ID is provided as an argument
if [ $# -eq 0 ]; then
  echo "Usage: $0 <pubmed_id1> <pubmed_id2> ..."
  exit 1
fi

mkdir -p ./research_papers
cd ./research_papers

# Iterate through the command-line arguments
for f in "$@"; do
  PMCID=$(wget  --user-agent="Mozilla/5.0 (Windows NT 5.2; rv:2.0.1) Gecko/20100101 Firefox/4.0.1" \
   -l1 --no-parent "${Link}${f}" -O - 2>/dev/null | grep -Eo 'PMC[0-9]+' | head -n 1)

    if [ "$PMCID" ]; then
       wget  --user-agent="Mozilla/5.0 (Windows NT 5.2; rv:2.0.1) Gecko/20100101 Firefox/4.0.1" \
            -l1 --no-parent -A.pdf "${PMCLink}${PMCID}/pdf/" -O "${f}.pdf" 2>/dev/null
    else
       echo "No PMC ID for $f"
    fi

done

echo "Finished processing IDs."