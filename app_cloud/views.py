from django.shortcuts import render
from app_home.models import User

# Create your views here.

# Index HTML
def cloud_index(request):
    if 'id' in request.session:
        id = request.session['id']
        user = User.objects.get(id=id) 

        return render(request, 'cloud_home.html', {'username': user.username, 'email': user.email, 'date': user.date.strftime("%d/%m/%y")})