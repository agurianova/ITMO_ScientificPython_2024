import requests
import re
import json


# 1. first task 

## 1.1. get response

### 1.1.1. for uniprot
def get_uniprot(ids: list):
  accessions = ','.join(ids)
  endpoint = "https://rest.uniprot.org/uniprotkb/accessions"
  http_function = requests.get
  http_args = {'params': {'accessions': accessions}}
  
  return http_function(endpoint, **http_args)

### 1.1.2. for ensembl 
def get_ensembl(ids: list):
    accessions = {"ids": ids}
    endpoint = "https://rest.ensembl.org/lookup/id"
    http_function = requests.post
    http_args =  {'headers': {"Content-Type": "application/json"}, 'data': json.dumps(accessions)}

    return http_function(endpoint, **http_args)

## 1.2. parse response

### 1.2.1. for uniprot
def parse_response_uniprot(resp: dict):
    resp = resp.json()
    resp = resp["results"]
    output = {}
    for val in resp:
        acc = val['primaryAccession']
        species = val['organism']['scientificName']
        gene = val['genes']
        seq = val['sequence']
        output[acc] = {'organism':species, 'geneInfo':gene, 'sequenceInfo':seq, 'type':'protein'}

    return output

### 1.2.2. for ensembl 
def parse_response_ensembl(resp: dict):
    resp = resp.json()
    output = {}
    for val in resp.values():
        id = val['id']
        species = val['species']
        gene = {
            'biotype':val['biotype'],
            'description':val['description']
        }
        transcript = {
            'assembly_name':val['assembly_name'],
            'canonical_transcript':val['canonical_transcript'],
            'start':val['start'],
            'end':val['end']
        }
        sequence = {
            'assembly_name':val['assembly_name'],
            'start':val['start'],
            'end':val['end']
        }
        output[id] = {'speciesInfo': species, 'geneInfo': gene, 'transcriptInfo': transcript, 'sequenceInfo': sequence}

    return output


# 2. second task

def get_info(ids: list):

    regex_uniprot = "[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"
    regex_ensembl = "ENS[A-Z]+[0-9]{11}|[A-Z]{3}[0-9]{3}[A-Za-z](-[A-Za-z])?|CG[0-9]+|[A-Z0-9]+\.[0-9]+|YM[A-Z][0-9]{3}[a-z][0-9]"
    
    if re.fullmatch(regex_uniprot, ids[0])!=None:
        print('Its uniprot!')
        return parse_response_uniprot(get_uniprot(ids))

    if re.fullmatch(regex_ensembl, ids[0])!=None:
        print('Its ensembl!')
        return parse_response_ensembl(get_ensembl(ids))