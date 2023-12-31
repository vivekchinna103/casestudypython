"""from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SimpleField, SearchIndex,SearchableField,SearchFieldDataType,SearchField
from dotenv import load_dotenv
import os
load_dotenv()
# Azure Cognitive Search endpoint and admin keyendpoint = os.getenv("SEARCH_API_ENDPOINT")
endpoint = os.getenv("SEARCH_API_ENDPOINT")
admin_key = os.getenv("SEARCH_API_KEY")
# Define the index schema
index_name = 'dlcasestudynew'

fields = [
    SearchField(name='id',type="Edm.String",key=True,filterable=True,searchable=True,sortable=True),
    SearchField(name='CaseStudyName', type=SearchFieldDataType.String ,filterable=True,searchable=True,sortable=True),
    SearchField(name='Account', type=SearchFieldDataType.String,filterable=True,searchable=True,sortable=True),
    SearchField(name='Vertical', type=SearchFieldDataType.String, filterable=True,searchable=True,sortable=True),
    SearchField(name='SolutionName', type=SearchFieldDataType.String,filterable=True,searchable=True,sortable=True),
    SearchField(name='ServiceOfferingMapping', type=SearchFieldDataType.String,filterable=True,searchable=True,sortable=True),
    SearchField(name='Status', type='Edm.String',filterable=True,searchable=True,sortable=True),
    SearchField(name='Dependency', type='Edm.String',filterable=True,searchable=True,sortable=True),
    SearchField(name='Remarks', type='Edm.String',searchable=True,sortable=True,filterable=True),
    SearchField(name='MetaData', type='Edm.String',filterable=True,searchable=True,sortable=True),
    SearchField(name='FileName', type='Edm.String',filterable=True,searchable=True,sortable=True),
    SearchField(name='Rating', type='Edm.String',filterable=True,searchable=True,sortable=True)
]


index = SearchIndex(name=index_name, fields=fields)

# Create the index
credential = AzureKeyCredential(admin_key)
index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
index_client.create_index(index)
"""