from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from ansible_runner import run 
import os

@api_view(['GET'])
def hello_world(request):
    return Response({'message':'Helloworld'})

class RunPlaybookView(APIView):
    def post(self, request):
        playbook_path= "/home/jagadeeshv/POC-fullcode/api1.yaml"
        result = run(playbook=playbook_path)
            
        status = result.status
        rc = result.rc
        stderr = ""
        stdout = ""
        for event in result.events:
            if event['event'] == 'runner_on_ok':
                stdout += event['stdout']
            elif event['event'] == 'runner_on_failed':
                stderr += event['stdout']

        response_data = {
            "status": status,
            "rc" : rc,
            "stderr": stderr,
            "stdout": stdout,
        }
        
        return Response(response_data)

@api_view(['POST'])
def stop_server(request):
    print(" stopping Django server.....")
    os.kill(os.getpid(),9)
    print("Django server stopped successfully")
    # return Response("Django server stopped successfully")