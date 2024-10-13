from django.http import HttpResponse
from django_user_agents.utils import get_user_agent

class BlockMobileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = get_user_agent(request)
        
        # Verifica se o dispositivo é móvel
        if user_agent.is_mobile:
            return HttpResponse('<h1>Acesso bloqueado para dispositivos móveis.</h1>', status=403)
        
        # Continua o processamento normal da requisição
        response = self.get_response(request)
        return response
