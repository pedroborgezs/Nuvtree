from django.shortcuts import render

# Create your views here.

# Index HTML
def cloud_index(request):
    return render(request, 'index.html')  # O HTML está em 'templates/app_cloud/index.html'