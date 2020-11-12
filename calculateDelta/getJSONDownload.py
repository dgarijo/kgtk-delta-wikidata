# method that reads an input CSV, retrieves metadata and derives the JSON download URL from the internet archive
# APIs.

import csv
import requests
import json

input_csv = "wd-dump-list-URL.tsv"
with open(input_csv, encoding="utf-8") as csvfile:

    tsv = csv.reader(csvfile, delimiter="\t")
    first_row = next(tsv)
    for r in tsv:
        # URLs are in the first row
        metadata_url = r[1].replace("details","metadata")
        # print(metadata_url)
        text_response = requests.get(metadata_url)
        item_id = metadata_url.rsplit('/', 1)[-1]
        # print (item_id)
        js = json.loads(text_response.text)
        try:
            json_dump_exists = False
            for item in js['files']:
                if "json.gz" in item['name'] or "json.bz2" in item['name'] :
                    print ("https://archive.org/download/" +item_id + "/"+ item['name'])
                    json_dump_exists = True;
                    break;
            if json_dump_exists != True:
                print("DOES NOT EXIST")
        except:
            print("ERROR/n")
        #print(json['files'])
       # print(r[1])