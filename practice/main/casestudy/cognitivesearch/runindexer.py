from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import  IndexingParameters,SearchIndexer
from dotenv import load_dotenv
import os
load_dotenv()

#endpoint = 'https://dlpractice.search.windows.net'
#admin_key = '37jMB2DPlxnGcEbeDnB66vlnXpbOwCFSJVOU7yU8uPAzSeA66uzd'
endpoint = os.getenv("SEARCH_API_ENDPOINT")
admin_key = os.getenv("SEARCH_API_KEY")
def runindex():
    credential = AzureKeyCredential(admin_key)
    indexer_client = SearchIndexerClient(endpoint=endpoint, credential=credential)
    indexer_client.run_indexer(name=os.getenv("INDEX_NAME"))
def run_azureblobindexer():
    credential = AzureKeyCredential(admin_key)
    indexer_client = SearchIndexerClient(endpoint=endpoint, credential=credential)
    indexer_client.run_indexer(name=os.getenv('INDEX_1'))
