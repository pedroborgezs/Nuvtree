# Arquivo que direciona para o HTML

# Modules
from .modules import methods_user

# Importa libs
from django.shortcuts import render, redirect

# Index HTML
def home(request):
    return render(request, 'index.html')

# Página de erro
def error(request):
    return render(request, 'error.html')

# Página de login
def sign_in(request):
    if request.method == "POST":
        error_message = methods_user.user_check(request)

        if "success" in error_message:
            return redirect('cloud_index')
        elif error_message:
            context = {
                'error_message': error_message,
            }
            return render(request, 'sign-in.html', context)

    return render(request, 'sign-in.html')

# Página de criar conta
def sign_up(request):
    if request.method == "POST":
        new_user, error_message = methods_user.user_validate(request)
        
        if error_message:
            context = {
                'error_message': error_message,
            }
            return render(request, 'sign-up.html', context)

        methods_user.user_send_email(new_user)

        request.session['verify_send_access'] = True
        return redirect('/verify/email')

    return render(request, 'sign-up.html')

# Página de verificação
def verify_send(request):
    if request.session.get('verify_send_access'):
        del request.session['verify_send_access']
        return render(request, 'verify/email.html')
    else:
        return redirect('/error')

# Envia a verificação para o e-mail 
def verify_email(request):
    return methods_user.user_verify_email(request)
