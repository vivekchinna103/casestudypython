from email.quoprimime import body_check
from inspect import BoundArguments
import re
from tkinter import VERTICAL
import datetime 
from django.conf import settings
from django.http import JsonResponse, QueryDict
from casestudy.cognitivesearch.oDatfilter import oDataFilter
from casestudy.cognitivesearch.aiFilter import aiFilter
from django.shortcuts import render
from operator import inv
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from rest_framework.parsers import JSONParser
from CaseStudyApp.models import CaseStudies
from django.core.files.storage import default_storage
from CaseStudyApp.Serializers import CaseStudySerializers
from rest_framework import generics
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import json, os
from casestudy import connectdb
from casestudy.blobClient import upload
from casestudy import blobClient
from rest_framework.decorators import api_view
#ms_identity_web = settings.MS_IDENTITY_WEB



@csrf_exempt
#@ms_identity_web.login_required
def filter_endpoint(request):
    if request.method=="POST":
        body_content = request.body.decode('utf-8')
        body_content=json.loads(body_content)
        vertical = body_content.get('Vertical')
        account = body_content.get('Account')
        service_offering_mapping = body_content.get('ServiceOfferingMapping')
        metadata = body_content.get('MetaData')
        rating = body_content.get('Rating')
        customer_reference=body_content.get('CustomerReferenceable')
        tag= body_content.get('Key')
        if vertical!=None:
            vertical= str(vertical)
        else:
            vertical=None
        if account!=None:
            account= str(account)
        else: 
            account=None
        if service_offering_mapping!=None:
            service_offering_mapping= str(service_offering_mapping)
        else:
            service_offering_mapping=None
        if metadata!=None:
            metadata= str(metadata)
        else:
            metadata=None
        if rating!=None:
            rating= str(rating)
        else:
            rating=None
        if customer_reference!=None:
            customer_reference=str(customer_reference)
        else:
            customer_reference=None
        if tag!=None:
            tag=str(tag)
        else:
            tag=None
        if tag==None:
            filtered_data = oDataFilter(account,vertical,service_offering_mapping,metadata,rating,customer_reference)
            return JsonResponse(filtered_data,safe=False)
        elif(account==None and vertical==None and service_offering_mapping==None and metadata==None and rating==None and customer_reference==None and tag!=None ):
            filename=aiFilter(tag)
            ans=[]
            for file in range(0 ,len(filename)):
                val= connectdb.getaiFiltereddata(filename[file])
                if (val!=None):
                    ans.append(val)
            #response = JsonResponse(ans, safe=False)
            #data = json.dumps(response.content.decode("utf-8"))  # Serialize the response data to JSON
            data= json.dumps(ans)
            return JsonResponse(json.loads(data), safe=False)
            #return JsonResponse(ans,safe=False)
        else:
            filename=aiFilter(tag)
            val=oDataFilter(account,vertical,service_offering_mapping,metadata,rating,customer_reference)
            ans=[]
            for value in range(0,len(val)):
                for file in range(0,len(filename)):
                    if (filename[file]==val[value]["FileName"]):
                        ans.append(val[value])
            data= json.dumps(ans)
            return JsonResponse(json.loads(data), safe=False)
            
        
    #service_offering_mapping = body_content.get('ServiceOfferingMapping', None)
    #metadata = body_content.get('MetaData', None)
    #rating = body_content.get('Rating', None)
    # Call the oDataFilter function passing the filter parameters
        #filtered_data = oDataFilter(account,vertical,service_offering_mapping,metadata,rating)
    # Return the filtered data as a JSON response
        #ssl._create_default_https_context = ssl._create_unverified_context
        #return JsonResponse(json.loads(filtered_data),safe=False)
        #return JsonResponse("error :invalid request method",status=405,safe=False)
@csrf_exempt
def get_case_id(request,id):
    if request.method=="GET":
        try:
            product=CaseStudies.objects.get(id=id)
            product_serializer= CaseStudySerializers(product)
            return JsonResponse(json.loads(json.dumps(product_serializer.data)),safe=False)
        except:
            return JsonResponse(("Sorry!  Your case id={} is not found!").format(id),safe=False)
@csrf_exempt
def get_all_cases(request):
    if request.method=="GET":
        results=connectdb.get_all()
        return JsonResponse(json.loads(json.dumps(results)), safe=False)
        #return JsonResponse(json.loads(json.dumps(product)), safe=False)
@csrf_exempt
def add_data_api(request):
    if request.method=="POST":
        body_content = request.POST
        #body_content=json.loads(body_content)
        #print(body_content)
        #body_content=json.loads(body_content)
        #body_content=json.loads(body_content)
        name=body_content.get('CaseStudyName')
        vertical = body_content.get('Vertical')
        account = body_content.get('Account')
        solution= body_content.get('SolutionName')
        spoc= body_content.get('spoc')
        status=body_content.get('Status')
        filename=body_content.get('FileName')
        year= body_content.get('Year')
        casestudy_poc=body_content.get('CaseStudyPOC')
        service_offering_mapping = body_content.get('ServiceOfferingMapping')
        metadata = body_content.get('MetaData')
        rating = body_content.get('Rating')
        customer_reference=body_content.get('CustomerReferenceable')
        dependency=body_content.get('Dependency')
        #remarks=body_content.get("Remarks")
        #print(name,account,vertical,solution,service_offering_mapping,status,dependency,remarks,metadata,filename,rating)
        if request.FILES:
            file=request.FILES["filename"]
        if filename==None or filename=="":
            filename=file.name
        
        connectdb.add_data(name,account,vertical,spoc,solution,service_offering_mapping,status,metadata,filename,rating,year,casestudy_poc,customer_reference,dependency)
        #add_data(name,account,vertical,solution,service_offering_mapping,status,dependency,remarks,metadata,filename,rating)
        file=request.FILES
        if(request.FILES):
            file=request.FILES['filename']
            upload(file,file.name)
        else:
            return JsonResponse("added succesfully but no file uploaded!",safe=False)
        return JsonResponse("added successfully and file is uploaded!",safe=False)


@api_view(['PUT'])
@csrf_exempt
def update_api(request,id):
    if request.method=="PUT":
        #body_content = request.body.decode('utf-8')
        #body_content=json.loads(body_content)
        body_content= request.data
        id=body_content.get('id')
        id=int(id)
        name=body_content.get('CaseStudyName')
        vertical = body_content.get('Vertical')
        account = body_content.get('Account')
        solution= body_content.get('SolutionName')
        spoc= body_content.get('spoc')
        status=body_content.get('Status')
        file_name=body_content.get('FileName')
        year= body_content.get('Year')
        casestudy_poc=body_content.get('CaseStudyPOC')
        service_offering_mapping = body_content.get('ServiceOfferingMapping')
        metadata = body_content.get('MetaData')
        rating = body_content.get('Rating')
        customer_reference=body_content.get('CustomerReferenceable')
        dependency=body_content.get('Dependency')
        if request.FILES:
            file=request.FILES["filename"]
        if file_name==None or file_name=="":
            file_name=file.name       
        connectdb.update_data(id, name, account, vertical, spoc, solution, service_offering_mapping, status, metadata, file_name, rating, year, casestudy_poc, customer_reference, dependency)
        file=request.FILES
        if(request.FILES):
            file=request.FILES['filename']
            upload(file,file.name)
        else:
            return JsonResponse("data updated successfully! no file!",safe=False)
        return JsonResponse("data updated successfully!",safe=False)
@csrf_exempt
def get_all_users_api(request):
    if request.method=="GET":
        result=connectdb.get_users()
        return JsonResponse(json.loads(json.dumps(result)), safe=False)
def get_auditlogs(request):
    if request.method=="GET":
        result=connectdb.audit_logs()
        return JsonResponse(json.loads(json.dumps(result)), safe=False)
def get_user_id(request,id):
    if request.method=="GET":
        #body_content = request.body.decode('utf-8')
        #body_content=json.loads(body_content)
        #id=body_content.get('id')
        result=connectdb.get_user(id)
        return JsonResponse(json.loads(json.dumps(result)),safe=False)
@csrf_exempt
def add_users(request):
    if request.method=="POST":
       body_content = request.body.decode('utf-8')
       body_content=json.loads(body_content)
       #body_content = request. 
       #body_content=json.loads(body_content)
       user_name=body_content.get('Name1')
       user_email=body_content.get('Email1')
       user_status=body_content.get('Status1')
       #print(body_content)
       if(user_status)=="":
           user_status='2'
       connectdb.add_users(user_name,user_email,user_status)
       return JsonResponse("added!",safe=False)
       #print(body_content)
       #connectdb.add_users(user_name,user_email,user_status)
       #return JsonResponse(json.loads(json.dumps(body_content)),safe=False)
@csrf_exempt
def edit_users(request,id):
    if request.method=="PUT":
       body_content = request.body.decode('utf-8')
       body_content=json.loads(body_content)
       user_satus=body_content.get('Status')
       print(user_satus)
       try:
           connectdb.change_access_level(user_satus,id)
           #print(body_content)
           return JsonResponse("updated",safe=False)
       except:
           return JsonResponse("error occured updating status!",safe=False)

@csrf_exempt
def delete_user(request,id):
    if request.method=="PUT":
        try:
            connectdb.softDelete(id)
            return JsonResponse("deleted succeddfully!", safe=False)
        except:
            return JsonResponse("errror occured while deleting!",safe=False)



@csrf_exempt
def get_accounts(request):
    if request.method=="POST":
        body_content=request.POST
        vertical= body_content.get("Vertical")
        if vertical:
            vertical
        else:
            vertical=None
        if(vertical==None):
            result=connectdb.get_accounts()
            page=request.GET.get('page')
            limit=request.GET.get('limit')
            startIndex=(int(page)-1)*(int(limit))
            endIndex= (int(page))* (int(limit))
            #print(result)
            length=len(result)
            #print(length)
            final=[]
            result=result[startIndex:endIndex]
            final.append(result)
            final.append(length)
            
            return JsonResponse(json.loads(json.dumps(final)),safe=False)
        else:
            result=connectdb.get_acounts2(vertical)
            page=request.GET.get('page')
            limit=request.GET.get('limit')
            startIndex=(int(page)-1)*(int(limit))
            endIndex= (int(page))* (int(limit))
            length=len(result)
            #print(length)
            final=[]
            result=result[startIndex:endIndex]
            final.append(result)
            final.append(length)
            return JsonResponse(json.loads(json.dumps(final)),safe=False)
    

@csrf_exempt
def Download_image(request,id):
    if request.method=="GET":
        file_name=connectdb.get_file(id)
        response=blobClient.download(file_name)
        response['Content-Disposition'] = "attachment; filename=%s" % file_name
        return response
        
@csrf_exempt
def get_artifacts(request):
    if request.method=="GET":
        result=connectdb.get_artifacts()
        return JsonResponse(json.loads(json.dumps(result)),safe=False)
@csrf_exempt
def get_artifacts_id(request,id):
    if request.method=="GET":
        file_name=connectdb.get_file2(id)
        response=blobClient.download2(file_name)
        response['Content-Disposition'] = "attachment; filename=%s" % file_name
        return response

