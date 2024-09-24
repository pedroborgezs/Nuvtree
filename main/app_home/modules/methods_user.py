# Importa libs
import re
from pathlib import Path
from ..models import User

# Libs do django pra alternância entre as páginas
from django.shortcuts import render, redirect

# user_validate
from django.contrib.auth.hashers import make_password

# user_send_email
from django.urls import reverse
from django.utils.http import urlencode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# user_verify_email
from django.http import HttpResponse

# user_check
from django.contrib.auth.hashers import check_password

def cloud_redirect():
    return redirect('cloud/index.html')

# Valida os dados do usuário
def user_check(request):
    # Cria o new_user com base no models User que esta no arquivo models.py
    user_to_check = User()

    # Coleta as informações do formulário POST do front
    # Grava as informações no modelo User
    user_to_check.username = request.POST.get('email-address') # Pode ser nome ou e-mail
    user_to_check.password = request.POST.get('password')

    # Verifica se existe essa conta no banco de dados
    # Por username
    user_exists = User.objects.filter(email=user_to_check.username).exists()

    # Se caso não existir, dê erro no front
    if not user_exists:
        error_message = "Incorrect e-mail or password!"
        return error_message
    
    # Verificar se a senha corresponde
    # Coleta os dados do e-mail que foi inserido
    user_exists = User.objects.get(email=user_to_check.username)

    if check_password(user_to_check.password, user_exists.password):
        if user_exists.is_active:
            return cloud_redirect()
        else:
            error_message = "The account is not active. Check your email!"
            return error_message
        
    else:
        error_message = "Incorrect e-mail or password!"
        return error_message
    
# Valida os dados do usuário
def user_validate(request):
    # Cria o new_user com base no models User que esta no arquivo models.py
    new_user = User()

    # Coleta as informações do formulário POST do front
    # Grava as informações no modelo User
    new_user.username = request.POST.get('username')
    new_user.email = request.POST.get('email-address')
    new_user.password = request.POST.get('password')
    new_user.confirm_password = request.POST.get('confirm-password')

    # Váriavel para verificar erros
    error_message = None

    # Verificações também acontecem no backend para melhor segurança
    # Se caso o username for menor que 5 caracteres
    if len(new_user.username) < 5:
        error_message = 'Username must be more than 5 characters'
        return None, error_message  
    
    # Verificar se o e-mail esta no formato certo
    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$' # example@gmail.com
    if not re.match(email_pattern, new_user.email):
        error_message = 'Invalid e-mail'
        return None, error_message  

    # Se caso a password for menor que 8 caracteres
    # E se a password corresponde com a confirm password
    if len(new_user.password) < 8:
        error_message = 'Password must be more than 8 characters'
        return None, error_message  
    elif new_user.password != new_user.confirm_password:
        error_message = 'Password does not match'
        return None, error_message  
    
    # Criptografar a senha
    new_user.password = make_password(new_user.password)

    # Verifica se o e-mail já está registrado no banco de dados
    if User.objects.filter(email=new_user.email).exists():
        error_message = 'This e-mail is already registered'
        return None, error_message  
    
    new_user.is_active = True

    new_user.save()  # Agora new_user só será salvo se não houver erros    
    return new_user, None  # Retornar new_user e None caso não tenha erro

# Envia mensagem para validar o email
def user_send_email(new_user):
    # Cria o token para a validação
    token = urlsafe_base64_encode(force_bytes(new_user.pk))

    # Cria a URL que será usada para o usurário validar o e-mail
    verification_url = reverse('success') + '?' + urlencode({'token': token})

    # Django settings file
    parent = Path(__file__).resolve().parent.parent.parent.parent
    settings_file = parent / "settings.conf"

    # Endereço IP do servidor
    with open(settings_file, 'r') as f:
        for line in f:
            if line.startswith("server_ip="):
                server_ip = line.split('=')[1].strip()
    local_ip = server_ip

    # URL inteira com o endereço do servidor
    # Por enquanto na mensagem só irá aparecer o verification_url
    verification_url = f"http://{local_ip}:8000{verification_url}"

    # Corpo do e-mail
    # Assunto
    mail_subject = 'Verify Your Account!'

    # Mensagem
    message = render_to_string('verify/message.html', {
        'user': new_user,
        'verification_url': verification_url,
    })

    # Incrementando no formulário de e-mail
    email = EmailMessage(
        subject=mail_subject,
        body=message,
        from_email='nuvtree@outlook.com',
        to=[new_user.email],
    )

    # Tipo do e-mail, por padrão deixe html a não ser que queira fazer outro tipo de formato
    email.content_subtype = 'html'

    # Envia o e-mail
    email.send()

# Recebe a confimação do email
def user_verify_email(request):
    # Coleta o token do link
    token = request.GET.get('token')    

    if not token:
        return redirect('/error')
    
    try:
        # Coleta o ID do usuário (link)
        new_user_id = urlsafe_base64_decode(token).decode()

        # Compara com um ID do banco de dados
        new_user = User.objects.get(pk=new_user_id)

        # Se encontar o usuário, define como ativo no banco de dados
        if new_user:
            new_user.is_active = True

            # Salva as novas alterações
            new_user.save()

            # Redireciona para a página de sucesso
            return render(request, 'verify/success.html')
        else:
            return render(request, 'verify/expired.html')

    # Se caso tudo der errado, aparece isso    
    except Exception:
        return render(request, 'verify/expired.html')
    
