from loader import load_from_pdf , load_from_riskdata
from langchain_community.vectorstores import FAISS
from  langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv()
VECTORSTORE_PATH = Path(os.getenv("VECTORSTORE_PATH"))
EMBEDDINGS_MODEL = 'aminhaeri/risk-embed'

def load_all_docs():
	risk_data_train, risk_data_test = load_from_riskdata() 
	pdf_docs = load_from_pdf([ 'basel_iii.pdf','gdpr.pdf','mifid_ii.pdf','finra_aml.pdf'])
	all_docs = risk_data_train+pdf_docs
	print(f"RiskData: {len(risk_data_train)} chunks")
	print(f"PDFs: {len(pdf_docs)} chunks")  
	print(f"Total: {len(all_docs)} chunks")		
	return all_docs
def get_embeddings():
	embeddings = HuggingFaceEmbeddings(
		model_name=EMBEDDINGS_MODEL, model_kwargs={'device':'cuda'},encode_kwargs={'normalize_embeddings':True}
	)
	return embeddings
def index_(documents):
	embeddings=get_embeddings()
	vec_store = FAISS.from_documents(documents,embeddings)
	VECTORSTORE_PATH.parent.mkdir(parents=True,exist_ok=True)
	vec_store.save_local(str(VECTORSTORE_PATH))
	print("VECTORSTORE_DONE")
	return vec_store


if __name__ == '__main__':
	all_docs =load_all_docs()
	index_(all_docs)
	#print(f'Risk Data \n {all_docs[0]} \n \n PDF_docs \n {all_docs[1]}')
