#!/usr/bin/python3
import requests
import pathlib
from time import sleep
from EdgarQuery import edgarQuery  

queryParams = {
  'CIK': '0000320193',
  'doc_type': '10-q'
}

cik, queryResult = edgarQuery(**queryParams)
pathlib.Path(fr'./reports/{cik}').mkdir(parents=True, exist_ok=True)

for accession_num in queryResult:
  if queryResult[accession_num]['file_info']['xbrl_href_present']:
    accessionNumSplit = accession_num.split('-')
    accessionNumJoined = ''.join(accessionNumSplit)
    endpoint = fr"https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumJoined}/Financial_Report.xlsx"
    response = requests.get(endpoint, timeout=5)
    print(f"{accession_num}: {response.status_code}")
    
    if (response.status_code != 200):
      try: 
        response = requests.get(endpoint[0:-1])
        print(f"{accession_num}: {response.status_code}")
        with open(fr"./reports/{cik}/{accessionNumJoined}.xls", 'wb') as report:
          report.write(response.content)
      except:
        raise FileNotFoundError('File not found at ' + endpoint) 
    else:
      with open(fr"./reports/{cik}/{accessionNumJoined}.xlsx", 'wb') as report:
          report.write(response.content)
    sleep(0.2)    
