from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.Proveedores.models import tb_proveedor
from apps.Proveedores.forms import ProveedorForm
from apps.UserProfile.models import tb_profile
from apps.scripts.validatePerfil import validatePerfil

#datos para la vista principal arriba de las citas y los ingresos.
from django.db.models import Count, Min, Sum, Avg
from datetime import date 
from apps.Turn.models import tb_turn
from apps.Caja.models import tb_ingreso
from apps.Caja.models import tb_egreso
# enviar correos
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from apps.ReservasWeb.models import tb_reservasWeb

# Create your views here.
@login_required(login_url = 'Demo:login' )
def ListProveedores(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]

	proveedores = tb_proveedor.objects.all()
	#queryset 
	reservas_hoy = tb_reservasWeb.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='Confirmada').count()
	turnos__hoy =  tb_turn.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='Confirmada').count()
	turnos_hoy = reservas_hoy + turnos__hoy
	ingresos_hoy = tb_ingreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	egresos_hoy  = tb_egreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	context = {
	'perfil':perfil,
	'proveedores':proveedores,
	'turnos_hoy':turnos_hoy,
	'ingresos_hoy':ingresos_hoy,
	'egresos_hoy':egresos_hoy,

	}


	return render (request, 'Proveedores/ListProveedores.html', context)


@login_required(login_url = 'Demo:login' )
def NuevoProveedor(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	Form = ProveedorForm
	fallido = None
	if request.method == 'POST':
		Form = ProveedorForm(request.POST or None)

		proveedor = tb_proveedor()
		proveedor.user = request.user
		if request.POST['email'] == '':
			proveedor.email = 'sin@descripcion.com'
		if request.POST['email'] != '':
			proveedor.email = request.POST['email']
		if request.POST['nameProveedor'] == '':
			proveedor.nameProveedor = 'Sin Descripcion'
		if request.POST['nameProveedor'] != '':
			proveedor.nameProveedor = request.POST['nameProveedor']
		if request.POST['cuit'] == '':
			proveedor.cuit = 000000
		if request.POST['cuit'] != '':
			proveedor.cuit = int(request.POST['cuit'])
		if request.POST['personaACargo'] == '':
			proveedor.personaACargo = 'Sin Descripcion'
		if request.POST['personaACargo'] != '':
			proveedor.personaACargo = request.POST['personaACargo'] 
		if request.POST['phoneNumberProveedor'] == '':
			proveedor.phoneNumberProveedor = 'Sin Descripcion'
		if request.POST['phoneNumberProveedor'] != '':
			proveedor.phoneNumberProveedor = request.POST['phoneNumberProveedor'] 
		if request.POST['paginaWeb'] == '':
			proveedor.paginaWeb = 'http://www.sindescripcion.com/'
		if request.POST['paginaWeb'] != '':
			proveedor.paginaWeb = request.POST['paginaWeb']
		if request.POST['phoneNumberProveedorTwo'] == '':
			proveedor.phoneNumberProveedorTwo = 'Sin descripcion'
		if request.POST['phoneNumberProveedorTwo'] != '':
			proveedor.phoneNumberProveedorTwo = request.POST['phoneNumberProveedorTwo']	
		if request.POST['razonSocial'] == '':
			proveedor.razonSocial = 'Sin descripcion'
		if request.POST['razonSocial'] != '':
			proveedor.razonSocial = request.POST['razonSocial']	
		if request.POST['urlPhoto'] == '':
			proveedor.urlPhoto = 'http://www.sindescripcion.com/'
		if request.POST['urlPhoto'] != '':
			proveedor.urlPhoto = request.POST['urlPhoto']	
		if request.POST['addressProveedor'] == '':
			proveedor.addressProveedor = 'Sin descripcion'	
		if request.POST['addressProveedor'] != '':
			proveedor.addressProveedor = request.POST['addressProveedor']				
		proveedor.save()
			#mandar mensaje de nuevo usuario
			#Enviaremos los correos a el colaborador y al cliente 
			#cliente
		usuario = proveedor.email #trato de traer el colaborador del formulario
		email_subject_usuario = 'Multipoint Nuevo Proveedor'
		email_body_usuario = "Hola %s, gracias por formar parte de nuestra familia como proveedor" %(proveedor.nameProveedor)
		message_usuario = (email_subject_usuario, email_body_usuario , 'eventos@b7000615.ferozo.com', [usuario])
			#mensaje para apreciasoft
		email_subject_Soporte = 'Nuevo Proveedor Registrado'
		email_body_Soporte = "se ha registrado un nuevo proveedor satisfactoriamente con nombre %s para verificar ingrese aqui http://179.43.123.41:8000" %(proveedor.nameProveedor)
		message_Soporte = (email_subject_Soporte, email_body_Soporte , 'eventos@b7000615.ferozo.com', ['soporte@apreciasoft.com', 'reservas@boomeventos.com', 'mg.arreaza.13@gmail.com'])
		#enviamos el correo
		send_mass_mail((message_usuario, message_Soporte), fail_silently=False)
		mensaje = "Hemos Guardado de manera exitosa su nuevo proveedor"
		return render(request, 'Proveedores/NuevoProveedor.html' , {'Form':Form, 'perfil':perfil, 'mensaje':mensaje})		
	else:
		Form = ProveedorForm()
		
	return render(request, 'Proveedores/NuevoProveedor.html' , {'Form':Form, 'perfil':perfil, 'fallido':fallido})



@login_required(login_url = 'Demo:login' )
def EditarProveedor(request, id_proveedor):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	proveedorEditar= tb_proveedor.objects.get(id=id_proveedor)
	fallido = None
	if request.method == 'GET':
		Form= ProveedorForm(instance = proveedorEditar)
	else:
		Form = ProveedorForm(request.POST, instance = proveedorEditar)
		proveedorEditar.user = request.user
		if request.POST['email'] == '':
			proveedorEditar.email = 'sin@descripcion.com'
		if request.POST['email'] != '':
			proveedorEditar.email = request.POST['email']
		if request.POST['nameProveedor'] == '':
			proveedorEditar.nameProveedor = 'Sin Descripcion'
		if request.POST['nameProveedor'] != '':
			proveedorEditar.nameProveedor = request.POST['nameProveedor']
		if request.POST['cuit'] == '':
			proveedorEditar.cuit = 000000
		if request.POST['cuit'] != '':
			proveedorEditar.cuit = int(request.POST['cuit'])
		if request.POST['personaACargo'] == '':
			proveedorEditar.personaACargo = 'Sin Descripcion'
		if request.POST['personaACargo'] != '':
			proveedorEditar.personaACargo = request.POST['personaACargo'] 
		if request.POST['phoneNumberProveedor'] == '':
			proveedorEditar.phoneNumberProveedor = 'Sin Descripcion'
		if request.POST['phoneNumberProveedor'] != '':
			proveedorEditar.phoneNumberProveedor = request.POST['phoneNumberProveedor'] 
		if request.POST['paginaWeb'] == '':
			proveedorEditar.paginaWeb = 'http://www.sindescripcion.com/'
		if request.POST['paginaWeb'] != '':
			proveedorEditar.paginaWeb = request.POST['paginaWeb']
		if request.POST['phoneNumberProveedorTwo'] == '':
			proveedorEditar.phoneNumberProveedorTwo = 'Sin descripcion'
		if request.POST['phoneNumberProveedorTwo'] != '':
			proveedorEditar.phoneNumberProveedorTwo = request.POST['phoneNumberProveedorTwo']	
		if request.POST['razonSocial'] == '':
			proveedorEditar.razonSocial = 'Sin descripcion'
		if request.POST['razonSocial'] != '':
			proveedorEditar.razonSocial = request.POST['razonSocial']	
		if request.POST['urlPhoto'] == '':
			proveedorEditar.urlPhoto = 'http://www.sindescripcion.com/'
		if request.POST['urlPhoto'] != '':
			proveedorEditar.urlPhoto = request.POST['urlPhoto']	
		if request.POST['addressProveedor'] == '':
			proveedorEditar.addressProveedor = 'Sin descripcion'	
		if request.POST['addressProveedor'] != '':
			proveedorEditar.addressProveedor = request.POST['addressProveedor']				
		proveedorEditar.save()
		mensaje = 'hemos guardado de manera exitosa tus nuevos datos'
		return render (request, 'Proveedores/NuevoProveedor.html' , {'Form':Form, 'perfil':perfil, 'mensaje':mensaje})
	return render (request, 'Proveedores/NuevoProveedor.html' , {'Form':Form, 'perfil':perfil, 'fallido':fallido})


@login_required(login_url = 'Demo:login' )
def EliminarProveedor(request, id_proveedor):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	proveedorBorrar= tb_proveedor.objects.get(id=id_proveedor)
	fallido = None
	if request.method == 'POST':
		proveedorBorrar.delete()
		mensaje = 'Hemos Borrado manera exitosa todos sus registros'
		return render (request, 'Proveedores/DeteteProveedores.html', {'proveedorBorrar':proveedorBorrar, 'perfil':perfil, 'mensaje':mensaje})
	return render (request, 'Proveedores/DeteteProveedores.html', {'proveedorBorrar':proveedorBorrar, 'perfil':perfil})





########################Servicios###########################
from rest_framework import viewsets
from apps.Proveedores.serializers import ProveedorSerializer

class ProveedoresViewset(viewsets.ModelViewSet):
	queryset = tb_proveedor.objects.all()
	serializer_class = ProveedorSerializer