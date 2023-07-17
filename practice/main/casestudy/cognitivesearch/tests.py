from concurrent.futures.process import _ThreadWakeup
from pydoc import Doc
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import json
from azure.search.documents.indexes.models import  IndexingParameters,SearchIndexer
from azure.core.pipeline.transport import RequestsTransport
import datetime
endpoint = 'https://case-study-search.search.windows.net'
admin_key="DDghOcnFbOjOb7ipzZZBqa0xAuTkQVGtEWM9BWQZmXAzSeDtdMW7"

index_name = ''
credential = AzureKeyCredential(admin_key)
transport=RequestsTransport(connection_verify=False)
search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)
def test(location,date1,date2):
    val=[]
    flag=False
    query=""
    if location!=None:
        query=query+f"location eq {location}"
        flag=True
    if date2!=None and date1==None:
        if flag!=True:
            query=query+f"year gt {date2.isoformat()} and year le {date1.isoformat()}"
            flag=True
        else:
            query=query+ f" and year gt {date2.isoformat()} and year le {date1.isoformat()}"
    if (date2!=None and date1==None):
        if flag!=True:
            query=query+f"year lt {date2.isoformat()}"
            flag=True
        else:
            query=query+f" and year lt {date2.isoforamt()}"
    results= search_client.search(search_text='',filter=query,select="id,location,year")
    result_data = [dict(result) for result in results]
    json_data= json.dumps(result_data)
    return json.loads(json_data)

