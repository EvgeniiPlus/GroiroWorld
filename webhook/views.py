from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import hmac
import hashlib


@csrf_exempt
def deploy(request):
    if request.method == 'POST':
        # Запуск скрипта деплоя
        subprocess.call(['/var/www/services.pystart.by/GroiroWorld/deploy.sh'])
        return HttpResponse('Webhook received and deploy script executed.', status=200)
    else:
        return HttpResponse('Invalid request method.', status=400)
