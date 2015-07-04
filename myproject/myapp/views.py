# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm
import axmlparserpy.apk as apk

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from myproject.myapp.MyModelSerializer import MyModelSerializer


        
    

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            

          
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    for doc in documents :
        try:
            ap = apk.APK(doc.docfile.path)
            doc.packagename = ap.get_package()
            doc.version =  ap.get_androidversion_name()
            #doc.save()
        except Exception, e:
            doc.delete()
       
    
    # Render list page with the documents and the form
    return render_to_response(
        'myapp/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
    
def api(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Document.objects.all()
        for doc in snippets :
            try:
                ap = apk.APK(doc.docfile.path)
                doc.packagename = ap.get_package()
                doc.version =  ap.get_androidversion_name()
            except Exception, e:
                doc.delete()
        serializer = MyModelSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        
        return JSONResponse(serializer.errors, status=400)   
        
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        HttpResponse.__init__(self,content, **kwargs)