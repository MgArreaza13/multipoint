from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from apps.Inflacion.models import tb_inflacion

from apps.Inflacion.forms import InflacionForm
from apps.scripts.validatePerfil import validatePerfil
from apps.UserProfile.models import tb_profile

# Create your views here.


def reajuste(request):
	
	mes = int(request.GET.get('mes', None))
	query =  tb_inflacion.objects.all()
	registro = query[0]
	if mes == 1:
		inlacion_mes = registro.Enero
	elif mes == 2 :
		inlacion_mes = registro.Febrero
	elif mes == 3 :
		inlacion_mes = registro.Marzo
	elif mes == 4 :
		inlacion_mes = registro.Abril
	elif mes == 5 :
		inlacion_mes = registro.Mayo
	elif mes == 6 :
		inlacion_mes = registro.Junio
	elif mes == 7 :
		inlacion_mes = registro.Julio
	elif mes == 8 :
		inlacion_mes = registro.Agosto
	elif mes == 9 :
		inlacion_mes = registro.Septiembre
	elif mes == 10 :
		inlacion_mes = registro.Octubre
	elif mes == 11 :
		inlacion_mes = registro.Noviembre
	elif mes == 12 :
		inlacion_mes = registro.Diciembre
	
	print(inlacion_mes)
	data = {
        'value':inlacion_mes,
        

    }
	return JsonResponse(data)

######crud de inflacion ######
@login_required(login_url = 'Demo:login' )
def NuevoRegistroDeInflacion(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	Form = InflacionForm
	if request.method == 'POST':
		Form = InflacionForm(request.POST or None)
		if Form.is_valid():
			tipoTurn = Form.save(commit=False)
			tipoTurn.user = request.user
			tipoTurn.save()
			return redirect('Configuracion:Configuracion')
		else:
			Form = InflacionForm()
	return render(request, 'Inflacion/NuevoRegistroInflacion.html' , {'Form':Form, 'perfil':perfil})

@login_required(login_url = 'Demo:login' )
def EditarReistroDeInflacion(request, id_registro):
	RegistroDeInflacion= tb_inflacion.objects.get(id=id_registro)
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	if request.method == 'GET':
		Form= InflacionForm(instance = RegistroDeInflacion)
	else:
		Form = InflacionForm(request.POST, instance = RegistroDeInflacion)
		if Form.is_valid():
			tipoTurn = Form.save(commit=False)
			tipoTurn.user = request.user
			tipoTurn.save()
			return redirect ('Configuracion:Configuracion')
	return render (request, 'Inflacion/NuevoRegistroInflacion.html' , {'Form':Form, 'perfil':perfil})

@login_required(login_url = 'Demo:login' )
def EliminarRegistroDeInflacion(request, id_registro):
	RegisrtoDelete= tb_inflacion.objects.get(id=id_registro)
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	if request.method == 'POST':
		RegisrtoDelete.delete()
		return redirect ('Configuracion:Configuracion')
	return render (request, 'Inflacion/RegistroDelete.html', {'RegisrtoDelete':RegisrtoDelete, 'perfil':perfil})

