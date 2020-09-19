#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import json

def edgarQuery(CIK, doc_type, dateb='', owner='exclude', start='', state='', output='atom', count=100, action='getcompany'):
  endpoint = r'https://www.sec.gov/cgi-bin/browse-edgar'

  #params for query
  param_dict = {
    'action': action,
    'CIK': CIK,
    'type': doc_type,
    'dateb': dateb,
    'owner': owner,
    'start': start,
    'state': state,
    'output': output,
    'count': count
  }

  response = requests.get(url = endpoint, params = param_dict)

  #print status code
  print(response.status_code)
  print(response.url)

  soup = BeautifulSoup(response.content, 'lxml')

  #find all entry tags
  entries = soup.find_all('entry')
  cik = soup.find('cik').text

  #init list for storage
  entry_dict = {}

  #loop through entries
  for entry in entries:
    #grab accession number (typo in xml, number spelled nunber)
    accession_num = entry.find('accession-nunber').text
    
    #create entry dictionary key: accession-number, val: 
    entry_dict[accession_num] = {}

    #store category info
    category_info = entry.find('category')
    entry_dict[accession_num]['category'] = {}
    entry_dict[accession_num]['category']['label'] = category_info['label']
    entry_dict[accession_num]['category']['scheme'] = category_info['scheme']
    entry_dict[accession_num]['category']['term'] = category_info['term']

    #store file info
    entry_dict[accession_num]['file_info'] = {}
    try:
      entry_dict[accession_num]['file_info']['act'] = entry.find('act').text
    except:
      entry_dict[accession_num]['file_info']['act'] = ''
    entry_dict[accession_num]['file_info']['file_number'] = entry.find('file-number').text
    entry_dict[accession_num]['file_info']['file_number_href'] = entry.find('file-number-href').text
    entry_dict[accession_num]['file_info']['filing_date'] = entry.find('filing-date').text
    entry_dict[accession_num]['file_info']['filing_href'] = entry.find('filing-href').text
    entry_dict[accession_num]['file_info']['filing_type'] = entry.find('filing-type').text
    entry_dict[accession_num]['file_info']['form_number'] = entry.find('film-number').text
    entry_dict[accession_num]['file_info']['form_name'] = entry.find('form-name').text
    entry_dict[accession_num]['file_info']['form_size'] = entry.find('size').text

    try:
      entry_dict[accession_num]['file_info']['xbrl_href'] = entry.find('xbrl_href').text
      entry_dict[accession_num]['file_info']['xbrl_href_present'] = True
    except:
      entry_dict[accession_num]['file_info']['xbrl_href'] = ''
      entry_dict[accession_num]['file_info']['xbrl_href_present'] = False

    entry_dict[accession_num]['request_info'] = {}
    entry_dict[accession_num]['request_info']['link'] = entry.find('link')['href']
    entry_dict[accession_num]['request_info']['title'] = entry.find('title').text
    entry_dict[accession_num]['request_info']['last_update'] = entry.find('updated').text
  
  return cik, entry_dict

def main():
  CIK = input('Enter CIK or ticker: ').strip()
  doc_type = input('(optional)Enter type of the document you are querying: (Default is 10-k) ').strip().lower()
  dateb = input('(optional)Enter the latest date for documents in yyyymmdd form: ').strip()
  owner = input('Enter ownership of document (choose one of exclude, include, only): (Default is exclude)').strip().lower()
  #start = input('(optional) Enter starting index of results: (Default is 0)').strip()
  #state = input('(optional)Enter the company\'s state: ').strip()
  #output = input('Enter returned data structure: (Default is atom)').strip().lower()
  #count = input('Enter number of results you want (max. 100): (Default is 100)').strip()
  
  while not CIK:
    print('Please enter valid CIK or ticker')
    CIK = input('Enter CIK: ').strip()
  
  if not doc_type:
    doc_type = '10-k'

  while len(dateb) != 0 and len(dateb) != 8:
    print('Invalid latest date')
    dateb = input('(optional)Enter the latest date for documents in yyyymmdd form: ').strip()
  
  if not owner:
    owner = 'exclude'
  
  else:
    while owner not in ['exclude', 'include', 'only']:
      print('Invalid ownership')
      owner = input('Enter ownership of document (choose one of exclude, include, only): (Default is exclude)').strip().lower()

  queryParams = {
    'CIK': CIK,
    'doc_type': doc_type,
    'dateb': dateb,
    'owner': owner
  }

  cik, queryResult = edgarQuery(**queryParams)

  with open(fr'{cik}_query.txt', 'w') as file:
    file.write(json.dumps(queryResult, indent=2))
  
if __name__ == "__main__":
  main()
  input()