from django.urls import re_path,path
import importlib

#from CaseStudyApp.viewss import get_all,get_all_cases,get_case_id
from .viewss import delete_user, get_case_id,get_all_cases
from django.urls import path, include, re_path
from CaseStudyApp import viewss,views
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from ms_identity_web.django.msal_views_and_urls import MsalViews
#msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()
urlpatterns=[
    path('allCases',viewss.get_all_cases,name="getallcasesapi"),
    path('add',viewss.add_data_api,name="add_data_api"),
    path('case/<int:id>/',viewss.get_case_id,name="get_caseid"),
    path('update/<int:id>',viewss.update_api, name='updatedata'),
    path('filter', viewss.filter_endpoint, name='filter'),
    path('users', viewss.get_all_users_api,name="getallusers"),
    path('auditlogs', viewss.get_auditlogs,name="getallauditlogs"),
    path('users/<int:id>',viewss.get_user_id,name="getuseriddata"),
    path('users/add',viewss.add_users,name="addinguserapi"),
    path('users/edit/<int:id>',viewss.edit_users,name="editinguserapi"),
    path('users/delete/<int:id>',viewss.delete_user,name="deleteuserapi"),
    path('image1/<int:id>',viewss.Download_image,name="imagedownloadapi"),
    path('accounts',viewss.get_accounts,name="getacounts"),
    path('artifacts',viewss.get_artifacts,name="artifactsapi"),
    path('artifacts/<int:id>',viewss.get_artifacts_id,name="artifactsdownloadapi"),
    #path('sign_in_status', views.index, name='status'),
    #path('token_details', views.token_details, name='token_details'),
    #path('call_ms_graph', views.call_ms_graph, name='call_ms_graph'),
    #path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),
      # re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)


