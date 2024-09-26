from django.shortcuts import render

# Create your views here.

# Index HTML
def cloud_index(request):
    if 'id_user' in request.session:
        user_id = request.session['id_user']
        username = request.session['username']
        
        # Aqui você pode buscar mais informações sobre o usuário no banco de dados se necessário
        # user = User.objects.get(id=user_id)  # Exemplo de busca de informações adicionais

        return render(request, 'cloud_home.html', {'username': username})