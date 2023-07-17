"""from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import SearchIndexerDataSourceConnection
from azure.search.documents.indexes.models import SqlIntegratedChangeTrackingPolicy
from azure.search.documents.indexes import SearchIndexerClient
from dotenv import load_dotenv
import os
load_dotenv()
# Azure Cognitive Search endpoint and admin key
endpoint = os.getenv("SEARCH_API_ENDPOINT")
admin_key = os.getenv("SEARCH_API_KEY")

# Define the Azure SQL data source connection
data_source_name = os.getenv('INDEX_NAME')
connection_string = os.getenv('DB_CONN_STR')
data_source = SearchIndexerDataSourceConnection(
    name="dlpractice",
    type="azuresql",
    connection_string=connection_string,
    container={"name": "case_studies"}
)

# Create the data source

credential = AzureKeyCredential(admin_key)
data_source_client = SearchIndexerClient(endpoint=endpoint, credential=credential)
data_source_client.create_data_source_connection(data_source)
"""