import os 
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from datasets import load_dataset
from dotenv import load_dotenv
load_dotenv()
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
RD_PATH = Path(os.getenv("RISK_DATA_PATH"))
ADD_PATH = Path(os.getenv("ADDITIONAL_PDF_PATH"))

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


	# text_splitter = RecursiveCharacterTextSplitter( chunk_overlap=chunk_overlap,chunk_size=chunksize)
	# if type(pdf_name) is list:
	# 	documents =[]
	# 	for pdf in pdf_name:
	# 		loader = PyPDFLoader(ADD_PATH/pdf)
	# 		pages = loader.load()
	# 		for page in pages:
	# 			page.metadata['source'] = pdf
	# 		docs= text_splitter.split_documents(pages)
	# 		documents.extend(docs)
	# else:
	# 	loader = PyPDFLoader(ADD_PATH/pdf_name)
	# 	pages = loader.load()
	# 	for page in pages:
	# 			page.metadata['source'] = pdf_name
	# 	documents= text_splitter.split_documents(pages)
def load_from_pdf(pdf_name,chunksize = 1000,chunk_overlap=100):
	""" pdf_name = 'pdf_1' or ['pdf1','pdf2' ,. ..] """
	text_splitter = RecursiveCharacterTextSplitter( chunk_overlap=chunk_overlap,chunk_size=chunksize)
	pdf_list = pdf_name if isinstance(pdf_name,list) else [pdf_name]
	documents=[]
	for pdf in pdf_list:
		loader = PyPDFLoader(ADD_PATH/pdf)
		pages = loader.load()
		for page in pages:
			page.metadata['source'] = pdf
		docs= text_splitter.split_documents(pages)
		documents.extend(docs) 
	
	return documents



if __name__ =='__main__':
	print('Testing Documents')
	te_doc,tr_doc = load_from_riskdata()
	print(f"Train Document \n {te_doc[1]} \n Test Document \n {tr_doc[1]} \n")
	print("Testing \n")
	docum = load_from_pdf('finra_aml.pdf')
	print(docum[1])