from django.shortcuts import render
from apps.scripts.validatePerfil import validatePerfil
from django.contrib.auth.decorators import login_required
# Create your views here.
from apps.Marketing.models import tb_mail
from apps.UserProfile.models import tb_profile
from django.http import HttpResponse
from apps.Client.models import tb_client_WEB
from django.core.mail import send_mail
from apps.Marketing.models import tb_mail


def enviarMasivamenteCorreo(request):
	status = 200
	clientes = tb_client_WEB.objects.all()
	message = ""
	asunto = request.GET.get('asunto', None)
	correo = request.GET.get('mail', None)
	
	for i in range(0,len(clientes)):
		
		send_mail(asunto,message,'eventos@b7000615.ferozo.com',[clientes[i].mail],fail_silently=True,html_message=correo) 
	correo_nuevo = tb_mail()
	correo_nuevo.Asunto = asunto
	correo_nuevo.Mailbody = correo
	correo_nuevo.user = request.user
	correo_nuevo.save()
	return HttpResponse(status)





@login_required(login_url = 'Panel:Login' )
def ObtenerMail(request, id_mail):
	correo = tb_mail.objects.get(id = id_mail)
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	contexto = {
	'correo':correo,
	'perfil':perfil
	}
	return render(request, 'Marketing/GetCorreo.html', contexto )




@login_required(login_url = 'Panel:Login' )
def VistaPrincipal(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	correos_enviados = tb_mail.objects.all()
	contexto = {
	'enviados':correos_enviados,
	'perfil':perfil
	}
	return render (request, 'Marketing/mailPrincipal.html' , contexto)

@login_required(login_url = 'Panel:Login' )
def NuevoCorreo(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	contexto = {
	'perfil':perfil
	}
	return render (request, 'Marketing/NewMail.html' , contexto)