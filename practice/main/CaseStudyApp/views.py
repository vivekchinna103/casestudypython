from CaseStudyApp.Serializers import CaseStudySerializers
from django.shortcuts import render
from operator import inv
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from CaseStudyApp.models import CaseStudies
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.conf import settings
import requests
from azure_ad_verify_token import verify_jwt
#from casestudy import templates
from rest_framework import generics
#ms_identity_web = settings.MS_IDENTITY_WEB
@csrf_exempt
def casestudyApi(request,id=0):
    if request.method=="GET":
        if id==0:
            product= CaseStudies.objects.all();
            product_serializer= CaseStudySerializers(product,many=True)
            return JsonResponse(product_serializer.data, safe=False)
        else:
            product=CaseStudies.objects.get(id=id)
            product_serializer= CaseStudySerializers(product)
            return JsonResponse(product_serializer.data,safe=False)

    elif request.method=="POST":
        Product_data = JSONParser().parse(request)
        #print(request)
        product_serializer = CaseStudySerializers(data=Product_data)
        #print(product_serializer.is_valid())
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse("Added Successfully!!", safe= False)
        return JsonResponse("Failed to add man!",safe= False)
    
    elif request.method=="PUT":
         Product_data= JSONParser().parse(request)
         product= CaseStudies.objects.get(id=Product_data['id'])
         product_serializer = CaseStudySerializers(product,data=Product_data)     
         if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse("updated successfully", safe= False)
         return JsonResponse("failed to do man", safe=False)
@csrf_exempt
def SaveFile(request):
    file= request.FILES['uploadedFile']
    file_name=default_storage.save(file.name,file)
    return JsonResponse(file_name,safe=False)


"""@csrf_exempt
def index(request):
    return render(request, 'auth/status.html')

@csrf_exempt
@ms_identity_web.login_required
def token_details(request):
    return render(request, 'auth/token.html')

@csrf_exempt
def call_ms_graph(request):
    access_token= request.headers.get('Authorization')
    graph = 'https://graph.microsoft.com/v1.0/users'
    authZ = f'Bearer {access_token}'
    results = requests.get(graph, headers={'Authorization': access_token}).json()
    return JsonResponse(results,safe=False)

    # trim the results down to 5 and format them.
    if 'value' in results:
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:5]
    else:
        results['value'] =[{'displayName': 'call-graph-error', 'id': 'call-graph-error'}]
    return render(request, 'auth/call-graph.html', context=dict(results=results))
@csrf_exempt
def example(request):
    if request.method=="GET":
        product= CaseStudies.objects.all();
        product_serializer= CaseStudySerializers(product,many=True)
        return JsonResponse(product_serializer.data, safe=False)"""