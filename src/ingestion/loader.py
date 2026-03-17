import os 
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from datasets import load_dataset
from dotenv import load_dotenv
load_dotenv()
import json
RD_PATH = Path(os.getenv("RISK_DATA_PATH"))

def load_from_riskdata():
	with open(RD_PATH / 'train_set.json','r') as file:
		train_dataset = json.load(file)
	train_document = []
	for key, value in train_dataset.items():
		doc = Document(
			page_content=value[2],
			metadata = {
				'id':value[0],'question':value[1]
			}
		)
		train_document.append(doc)
	with open(RD_PATH / 'test_set.json', 'r') as file:
		test_dataset = json.load(file)
		test_document = []
		for key, value in test_dataset.items():
			doc=Document(
				page_content=value[2],
				metadata={
					'id':value[0] , 'question':value[1]
				}
			)
			test_document.append(doc)
	return test_document,train_document
	


if __name__ =='__main__':
	print('Testing Documents')
	te_doc,tr_doc = load_from_riskdata()
	print(f"Train Document \n {te_doc[1]} \n Test Document \n {tr_doc[1]}")
