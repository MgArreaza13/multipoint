from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django

from apps.Service.models import tb_service
from apps.Product.models import tb_product
from apps.UserProfile.models import tb_profile


#datos para la vista principal arriba de las citas y los ingresos.
from django.db.models import Count, Min, Sum, Avg
from datetime import date 
from apps.Turn.models import tb_turn
from apps.Caja.models import tb_ingreso
from apps.Caja.models import tb_egreso

#script de validar el perfil
from apps.ReservasWeb.models import tb_reservasWeb

from apps.scripts.validatePerfil import validatePerfil









# Create your views here.
@login_required(login_url = 'Demo:login' )
def inicio(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	turnos = tb_turn.objects.all()
	ReservasWeb = tb_reservasWeb.objects.all()
	perfil = result[0]
	fecha = date.today()
	servicios = tb_service.objects.all()[:10]
	productos = tb_product.objects.all()[:10]
	dataturn = tb_turn.objects.filter(statusTurn__nameStatus = "Confirmada") #traigo todos los turnos 
	listturn = tb_turn.objects.filter(statusTurn__nameStatus = "Confirmada")[:10]
	reservas = tb_reservasWeb.objects.filter(statusTurn__nameStatus = "Confirmada")[:10]
	data = [] #creo la data que rendeare luego 
	ing = [] #ingresos chart
	egr = [] #egresos chart

	counte = 0
	queryingresos = tb_ingreso.objects.all()
	queryegresos = tb_egreso.objects.all()
	for mes in range(1,13): #mes variara de 1 a 12
		count = 0 #contador en cero luego de cada mes
		for fecha1 in range(0,len(dataturn)): # se ecargara de recorrer todo los turnos 
			if mes == dataturn[fecha1].dateTurn.month and fecha.year ==  dataturn[fecha1].dateTurn.year : # si la en el listdo de turnos hay uno igual al mes en curso aumentara el contador
				count += 1
		data.append(count) # agrego a la data la sumatoria de los turnos del mes en curso
	#ingreso
	for mes in range(1,13): #mes variara de 1 a 12
		counti = 0 #contador en cero luego de cada mes
		for fecha1 in range(0,len(queryingresos)): # se ecargara de recorrer todo los turnos 
			if mes == queryingresos[fecha1].dateCreate.month and fecha.year ==  queryingresos[fecha1].dateCreate.year : # si la en el listdo de turnos hay uno igual al mes en curso aumentara el contador
				counti = counti + queryingresos[fecha1].monto
		ing.append(counti)
	#egresos 

	for mes in range(1,13): #mes variara de 1 a 12
		counten = 0 #contador en cero luego de cada mes
		for fecha1 in range(0,len(queryegresos)): # se ecargara de recorrer todo los turnos 
			if mes == queryegresos[fecha1].dateCreate.month and fecha.year ==  queryegresos[fecha1].dateCreate.year : # si la en el listdo de turnos hay uno igual al mes en curso aumentara el contador
				counten = counten + queryegresos[fecha1].monto
		egr.append(counten)

	#queryset 
	turnos_hoy =  tb_turn.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='En Espera').count()
	ingresos_hoy = tb_ingreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	egresos_hoy  = tb_egreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	context = {
	'turnos':turnos,
	'ReservasWeb':ReservasWeb,
	'reservas':reservas,
	'listturn':listturn,
	'perfil':perfil,
	'servicios':servicios,
	'productos':productos,
	'fecha':fecha,
	'turnos_hoy':turnos_hoy,
	'ingresos_hoy':ingresos_hoy,
	'egresos_hoy':egresos_hoy,
	'data':data,
	'ing':ing,
	'egr':egr


	}
	return render (request, 'PanelPrincipal/index.html' , context)

def login(request):
	logout_django(request)
	mensaje = None
	if request.method=="POST":
		user = request.POST['Usuario']
		passw	=	request.POST['Password']
		usuario = authenticate(username=user , password = passw)
		if usuario is not None:
			login_django(request, usuario)
			return redirect('/')
		else:
			mensaje = "Usuario o password incorrectas"
	return render (request, 'PanelPrincipal/login.html', {'mensaje':mensaje})
def logout(request):
	logout_django(request)
	return redirect('Demo:login')


@login_required(login_url = 'Demo:login' )
def calendario(request):
	turnos = tb_turn.objects.filter(statusTurn__nameStatus="Confirmada")
	ReservasWeb = tb_reservasWeb.objects.filter(statusTurn__nameStatus="Confirmada")
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	fecha = date.today()
	perfil = result[0]
	servicios = tb_service.objects.all()[:10]
	turnos_hoy =  tb_turn.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='En Espera').count()
	ingresos_hoy = tb_ingreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	egresos_hoy  = tb_egreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))

	context = {
	'ReservasWeb':ReservasWeb,
	'servicios':servicios , 
	'fecha':fecha ,
	'turnos':turnos,
	'perfil':perfil,
	'turnos_hoy':turnos_hoy,
	'ingresos_hoy':ingresos_hoy,
	'egresos_hoy':egresos_hoy,
	}
	return render (request, 'PanelPrincipal/calendar.html' ,context)



@login_required(login_url = 'Demo:login' )	
def ingresosegresos(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	return render (request, 'PanelPrincipal/ingresos-egresos.html' , {'perfil':perfil})



def loockscreen(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	usuario =  request.user
	mensaje = None
	if request.method=="POST":
		user = usuario
		passw	=	request.POST['Password']
		usuario = authenticate(username=user , password = passw)
		if usuario is not None:
			return redirect('/')
		else:
			mensaje = "Usuario o password incorrectas"
	return render (request, 'PanelPrincipal/lookscreen.html' , {'mensaje':mensaje , 'perfil':perfil,'usuario':usuario})




@login_required(login_url = 'Demo:login' )
def registro(request):
	return render (request, 'PanelPrincipal/registro.html')































 
 
 