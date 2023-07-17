from datetime import datetime, timedelta, tzinfo
from tracemalloc import start
from typing import Container
from azure.storage.blob import BlobServiceClient, ContainerClient,generate_account_sas, AccountSasPermissions, ResourceTypes
from django.http import HttpResponse
import os,io
import os
from dotenv import load_dotenv
load_dotenv()

# Get the Azure Storage account name and key from environment variables
#account_name = 'cases1967'
#account_key = 'LLGNzoU4NTehiEcVFPKxPAmYhd7oaFR59p04N+d1tK9y2giVpBtmE2f0+nwuJ+u9UB2eA4jtbi8S+AStsddylw=='

account_name=os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
account_key=os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
account_url=f"https://{account_name}.blob.core.windows.net"
# Create a BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=account_key)


def get_url(blob):
    sas_token = create_account_sas()
    if not account_name:
        raise Exception('Azure storage account not found!')
    if not sas_token:
        raise Exception("Azure Storage accountkey not found!")
    blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)
    container_name = os.getenv("CONTAINER_NAME")
    blob_name=blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    return blob_client.url


def create_account_sas():
    # Set the SAS token options

# Configure the SAS token options
    sas_options = {
    #'services': AccountSasServices(blob=True, table=True, queue=True, file=True),
    'resource_types': ResourceTypes(object=True, container=True, service=True),
    'permissions': AccountSasPermissions(read=True,write=True, delete=True, list=True, add=True, create=True, update=True, process=True),
    'start': datetime.utcnow(),
    'expiry': datetime.utcnow() + timedelta(minutes=10),
    }

# Generate the SAS token
    sas_token = generate_account_sas(
      account_name=blob_service_client.account_name,
      account_key=blob_service_client.credential.account_key,
        resource_types=sas_options['resource_types'],
      #services=sas_options['services'],
     permission=sas_options['permissions'],
     expiry=sas_options['expiry'],
       )
    if sas_token[0]=="?":
        return sas_token
    else:
        return "?"+str(sas_token)
# Print the SAS token
    #print(sas_token)

def upload(file,file_name):
    sastoken=create_account_sas()
    if not account_name:
        raise Exception('Azure storage account not found!')
    if not sastoken:
        raise Exception("Azure Storage accountkey not found!")
    #blob_service_client=BlobServiceClient(account_url=account_url, credential=sastoken)
    container_name=os.getenv("CONTAINER_NAME")
    container_client=ContainerClient(account_url=account_url,container_name=container_name,credential=sastoken)
    stream=io.BytesIO(file.read())
    stream_length=len(stream.getbuffer())
    block_blob_client=container_client.get_blob_client(file.name)
    block_blob_client.upload_blob(stream,length=stream_length,overwrite=True)
    


def download(file):
    sas_token=create_account_sas()
    if not account_name:
        raise Exception('Azure storage account not found!')
    if not sas_token:
        raise Exception("Azure Storage accountkey not found!")
    blob_service_client=BlobServiceClient(account_url=account_url, credential=sas_token)
    container_name=os.getenv("CONTAINER_NAME")
    container_client=ContainerClient(account_url=account_url,container_name=container_name,credential=sas_token)
    block_blob_client= container_client.get_blob_client(file)
    blob_data=block_blob_client.download_blob()
    content = blob_data.readall()
    response = HttpResponse(content,content_type="mime_type")
    
    #response['Content-Disposition'] = f'attachment; filename={file}'
    return response

def download2(file):
    sas_token=create_account_sas()
    if not account_name:
        raise Exception('Azure storage account not found!')
    if not sas_token:
        raise Exception("Azure Storage accountkey not found!")
    blob_service_client=BlobServiceClient(account_url=account_url, credential=sas_token)
    container_name=os.getenv("NEW_CONTAINER_NAME")
    container_client=ContainerClient(account_url=account_url,container_name=container_name,credential=sas_token)
    block_blob_client= container_client.get_blob_client(file)
    blob_data=block_blob_client.download_blob()
    content = blob_data.readall()
    response = HttpResponse(content,content_type="mime_type")
    
    #response['Content-Disposition'] = f'attachment; filename={file}'
    return response
#print(create_account_sas())
#print(get_url("New presentation.pptx"))
