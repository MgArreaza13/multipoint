from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import date
from apps.ReservasWeb.models import tb_reservasWeb
#Modelos 
from apps.Turn.models import tb_turn
from apps.Collaborator.models import tb_collaborator
from apps.Turn.models import tb_turn
from apps.Caja.models import tb_ingreso
from apps.Caja.models import tb_egreso
from apps.Service.models import tb_service
from apps.Product.models import tb_product
#FORMULARIOS
from apps.ReservasWeb.forms import ReservasWebForm
from apps.ReservasWeb.forms import EditReservaWebForm
#datos para la vista principal arriba de las citas y los ingresos.
from django.db.models import Count, Min, Sum, Avg
from datetime import date 
# Create your views here.
from apps.UserProfile.models import tb_profile
from apps.scripts.validatePerfil import validatePerfil
from apps.Configuracion.models import tb_status
# enviar correos
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from datetime import date 
from django.http import JsonResponse
from apps.Notificaciones.models import Notificacion
from apps.Caja.forms import WebReservasIngresoForm
from ingenico.connect.sdk.factory import Factory
from apps.ingenico.MycheckoutSupport import Pago_Online
from apps.ingenico.MycheckoutSupport import statusDePago
from django.contrib import auth
from apps.Configuracion.models import tb_formasDePago
from apps.Configuracion.models import tb_tipoIngreso

from apps.scripts.SumarHora import sumar_hora






def validacion(request):
	id_servicio = request.GET.get('id_servicio', None)
	ser=tb_service.objects.filter(id=id_servicio)
	servicio = ser[0]
	data = {
        'value':servicio.priceList
    }
	return JsonResponse(data)


def returnPago(request):
	if request.method == "GET":
		print('miguel')
	return HttpResponse("ok")

def Status(request ):
	pk = request.GET.get('pk', None)
	
	reserva = tb_reservasWeb.objects.get(id= pk)
	status = (statusDePago(reserva.ingenico_id))
	data = {
        'status':status._GetHostedCheckoutResponse__status
    }
	return JsonResponse(data)


def StatusChange(request ):
	pk = request.GET.get('pk', None)
	reserva = tb_reservasWeb.objects.get(id= pk)
	reserva.isPay = True
	reserva.statusTurn =  tb_status.objects.get(nameStatus= 'Confirmada') 
	reserva.PagoOnline = True
	reserva.save()
	print(request.user)
	## hay que crear este usuario en la base de Datos 'ReservasWeb'
	user = auth.authenticate(username='ReservasWeb', password='miguel123')
	ingreso = tb_ingreso()
	ingreso.user = user
	ingreso.tipoPago = tb_formasDePago.objects.get(nameFormasDePago='Pago Online')
	ingreso.tipoIngreso = tb_tipoIngreso.objects.get(nameTipoIngreso='Servicios Web')
	ingreso.service = reserva.servicioPrestar
	ingreso.monto = reserva.montoAPagar
	ingreso.descripcion = 'Pagado desde el Motor de Pagos Online'
	ingreso.save()
	auth.logout(request)
	#mandar correo cuando se paga la reserva
	usuario = reserva.mail #trato de traer el colaborador del formulario
	email_subject_usuario = 'Multipoint - Gracias Por su Pago'
	email_body_usuario = "Hola %s, gracias por completar su pago de manera exitosa, hemos aprobado su solicitud ya de servicio , esperemos disfrute nuestros servicios" %(reserva.nombre)
	message_usuario = (email_subject_usuario, email_body_usuario , 'as.estiloonline@gmail.com', [usuario])
	#mensaje para apreciasoft
	email_subject_Soporte = 'Multipoint - Nueva Reserva WEB PAGADA'
	email_body_Soporte = "se ha registrado un Pago de una  reserva , nombre:%s . correo:%s, numero:%s , para un servicio %s, y un monto de $%s te invitamos a revisarla en http://multipoint.pythonanywhere.com/reservas/list/" %(reserva.nombre, reserva.mail, reserva.telefono, reserva.servicioPrestar, reserva.montoAPagar)
	message_Soporte = (email_subject_Soporte, email_body_Soporte , 'as.estiloonline@gmail.com', ['soporte@apreciasoft.com', "mg.arreaza.13@gmail.com"])
	#enviamos el correo
	send_mass_mail((message_usuario, message_Soporte), fail_silently=False)
	return HttpResponse('ok')


def Pago(request, id_reserva):
	reserva = tb_reservasWeb.objects.get(id=id_reserva)
	data = Pago_Online(reserva.montoAPagar)
	url = "https://payment."+data._CreateHostedCheckoutResponse__partial_redirect_url

	reserva.ingenico_id =data._CreateHostedCheckoutResponse__hosted_checkout_id
	
	reserva.save()
	return redirect(url)





@login_required(login_url = 'Demo:login' )
def ReservaWebPorPagar(request, id_reserva):
	reserva = tb_reservasWeb.objects.get(id=id_reserva)
	admin = tb_profile.objects.filter(tipoUser='Administrador')
	administrador = admin[0]
	fecha = date.today()
	Form = WebReservasIngresoForm
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	fallido = None
	if request.method == 'POST':
		Form = WebReservasIngresoForm(request.POST or None)
		if Form.is_valid():
			ingreso = Form.save(commit=False)
			ingreso.user = request.user
			ingreso.descripcion = "Pago de Reserva Web"
			ingreso.service = reserva.servicioPrestar
			ingreso.monto = reserva.montoAPagar
			ingreso.save()
			reserva.isPay = True
			reserva.save()
			mensaje = "Gracias Por registrar Su Pago"
			usuario = reserva.mail #trato de traer el colaborador del formulario
			email_subject_usuario = 'Multipoint - Gracias Por su Pago'
			email_body_usuario = "Hola %s, gracias por completar su pago de manera exitosa, esperemos disfrute nuestros servicios" %(reserva.nombre)
			message_usuario = (email_subject_usuario, email_body_usuario , 'as.estiloonline@gmail.com', [usuario])
			#mensaje para apreciasoft
			email_subject_Soporte = 'Multipoint - Nueva Reserva WEB PAGADA'
			email_body_Soporte = "se ha registrado un Pago de una  reserva , nombre:%s . correo:%s, numero:%s , te invitamos a contactarla y luego a cambiar el status de la reserva en  http://multipoint.pythonanywhere.com/reservas/list/" %(reserva.nombre, reserva.mail, reserva.telefono)
			message_Soporte = (email_subject_Soporte, email_body_Soporte , 'as.estiloonline@gmail.com', ['soporte@apreciasoft.com', "mg.arreaza.13@gmail.com"])
			#enviamos el correo
			send_mass_mail((message_usuario, message_Soporte), fail_silently=False)
			return render(request, 'ReservasWeb/FacturaPorPagar.html' , {'Form':Form, 'perfil':perfil, 'mensaje':mensaje, 'reserva':reserva,'administrador':administrador,'fecha':fecha,})
		else: 
			Form = WebReservasIngresoForm()
			fallido = "Hemos tenido algun problema con sus datos, por eso no hemos procesado su ingreso, verifiquelo e intentelo de nuevo"
			
	return render(request , 'ReservasWeb/FacturaPorPagar.html' , {'fallido':fallido,
			'Form':Form,
			'reserva':reserva,
			'administrador':administrador,
			'fecha':fecha,})


@login_required(login_url = 'Demo:login' )
def listReservas(request):
	TurnEditar = -1 #para poder saber que turnos se le mostrara el formulario, verifico que ningun id coincida con -1
	reservas = tb_reservasWeb.objects.all()
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	formulario = False
	#queryset 
	reservas_hoy = tb_reservasWeb.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='Confirmada').count()
	turnos__hoy =  tb_turn.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='Confirmada').count()
	turnos_hoy = reservas_hoy + turnos__hoy
	ingresos_hoy = tb_ingreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	egresos_hoy  = tb_egreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	context = {
	'perfil':perfil,
	'reservas':reservas,
	'turnos_hoy':turnos_hoy,
	'ingresos_hoy':ingresos_hoy,
	'egresos_hoy':egresos_hoy,
	'TurnEditar':TurnEditar,

	}
	return render(request,'ReservasWeb/listaDeReservas.html',context )

@login_required(login_url = 'Demo:login' )
def EditReservaList(request , id_reservas):
	formulario = True
	reservas = tb_reservasWeb.objects.all()
	ReservaWebEditar = tb_reservasWeb.objects.get(id = id_reservas)
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	if request.method == 'GET':
		idturn = id_reservas
		Form= EditReservaWebForm(instance=ReservaWebEditar)
	else:
		idturn = id_reservas
		Form= EditReservaWebForm(request.POST,instance=ReservaWebEditar)
		if  Form.is_valid():
			reserva 		 = Form.save(commit=False)
			reserva.dateTurn = ReservaWebEditar.dateTurn
			reserva.HoraTurn = ReservaWebEditar.HoraTurn
			reserva.mail = ReservaWebEditar.mail
			reserva.nombre = ReservaWebEditar.nombre
			reserva.servicioPrestar = ReservaWebEditar.servicioPrestar
			reserva.telefono = ReservaWebEditar.telefono
			reserva.montoAPagar =  ReservaWebEditar.montoAPagar
			reserva.description =  ReservaWebEditar.description
			reserva.isPay =  ReservaWebEditar.isPay
			reserva.save()
			print(reserva.statusTurn.nameStatus)
			if reserva.statusTurn.nameStatus == 'Confirmada':
				print('reserva confirmada email')
				email_subject_usuario = 'Reserva confirmada, motor de pago enviado'
				email_body_usuario = "Hola ha confirmado la reserva sera enviado el motor de pago mas informacion http://multipoint.pythonanywhere.com/" 
				message_usuario = (email_subject_usuario, email_body_usuario , 'as.estiloonline@gmail.com', ['soporte@apreciasoft.com', "mg.arreaza.13@gmail.com"])
				mail = reserva.mail
				email_subject_Soporte = 'Multipoint - Reserva Confirmada'
				email_body_Soporte = "hola %s, hemos confirmado tu reserva web te invitamos a procesar tu pago en http://multipoint.pythonanywhere.com/reservas/list/" %(reserva.nombre)
				message_Soporte = (email_subject_Soporte, email_body_Soporte , 'as.estiloonline@gmail.com', [mail])
				#enviamos el correo
				send_mass_mail((message_usuario, message_Soporte), fail_silently=False)
			return redirect ('Reservas:listReservas')
	return render (request, 'ReservasWeb/listaDeReservas.html', {'ReservaWebEditar':ReservaWebEditar,'reservas':reservas,'Form':Form , 'perfil':perfil})



def web(request):
	turnos = tb_turn.objects.filter(statusTurn__nameStatus="Confirmada")
	ReservasWeb = tb_reservasWeb.objects.filter(statusTurn__nameStatus="Confirmada")
	productos = tb_product.objects.all()
	servicios = tb_service.objects.all()
	Form = ReservasWebForm
	notificacion = Notificacion()
	fallido = None
	if request.method == 'POST':
		Form = ReservasWebForm(request.POST or None)
		if Form.is_valid():
			print(request.POST)
			turno = Form.save(commit=False)
			turno.dateTurn = request.POST['TurnDate']
			turno.HoraTurn = request.POST['TimeTurn']
			turno.statusTurn = tb_status.objects.get(nameStatus="Sin Aprobar")
			turno.servicioPrestar=tb_service.objects.get(id = request.POST['ServicioSeleccionado'])
			
			turno.montoAPagar = float(request.POST['total'])  
			turno.description = 'Sin Descripcion'
			turno.HoraTurnEnd = sumar_hora(request.POST['TimeTurn'], "3:00")
			turno.save()
			notificacion.nombre = turno.nombre
			notificacion.dateTurn = turno.dateTurn
			notificacion.save()
			turno_enviar = tb_reservasWeb.objects.get(id=turno.id)
			mensaje ="se ha registrado de forma correcta sus datos gracias por contactarnos"
			#mandar mensaje de nuevo usuario
			#Enviaremos los correos a el colaborador y al cliente 
			#cliente
			usuario = turno.mail #trato de traer el colaborador del formulario
			email_subject_usuario = 'Multipoint - Nueva Reserva'
			email_body_usuario = "Hola %s, gracias por solicitar una nueva reserva , para disfrutar de nuestros servicios te invitamos a resgistrarte aqui http://multipoint.pythonanywhere.com/" %(turno.nombre)
			message_usuario = (email_subject_usuario, email_body_usuario , 'as.estiloonline@gmail.com', [usuario])
			#mensaje para apreciasoft
			email_subject_Soporte = 'Multipoint - Nueva Reserva'
			email_body_Soporte = "se ha registrado una nueva reserva , nombre:%s . correo:%s, numero:%s , te invitamos a contactarla y luego a cambiar el status de la reserva en  http://multipoint.pythonanywhere.com/reservas/list/" %(turno.nombre, turno.mail, turno.telefono)
			message_Soporte = (email_subject_Soporte, email_body_Soporte , 'as.estiloonline@gmail.com', ['soporte@apreciasoft.com', "mg.arreaza.13@gmail.com"])
			#enviamos el correo
			send_mass_mail((message_usuario, message_Soporte), fail_silently=False)
			return redirect('Reservas:Factura', id_reservas=turno.id)
		else:
				fallido = "Errores en los datos Verifiquelos, y vuelva a intentarlo"
				Form = ReservasWebForm()
	return render(request, "ReservasWeb/reservasweb.html" , {'Form':Form,'servicios':servicios,'productos':productos ,'ReservasWeb':ReservasWeb ,'turnos':turnos ,'fallido':fallido,})


def Factura(request, id_reservas):
	reserva = tb_reservasWeb.objects.get(id=id_reservas)
	fecha = date.today()
	admin = tb_profile.objects.filter(tipoUser='Administrador')
	administrador = admin[0]

	
	return render(request, 'ReservasWeb/Confirmacion.html', {'reserva':reserva,'administrador':administrador ,'fecha':fecha})


@login_required(login_url = 'Demo:login' )
def DeleteReservas(request , id_reservas):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	ReservaBorrar = tb_reservasWeb.objects.get(id = id_reservas)
	if request.method == 'POST':
		ReservaBorrar.delete()
		mensaje = "hemos borrado sus datos de manera exitosa"
		return render (request, 'Turn/DeleteTurno.html', {'ReservaBorrar':ReservaBorrar, 'perfil':perfil, 'mensaje':mensaje})
	return render (request, 'ReservasWeb/DeleteReserva.html', {'ReservaBorrar':ReservaBorrar, 'perfil':perfil})



#########################SERVICIOS@#####################

from rest_framework import viewsets
from apps.ReservasWeb.serializers import ReservasWebSerializer

class ReservasWebViewsets(viewsets.ModelViewSet):
	queryset = tb_reservasWeb.objects.all()
	serializer_class = ReservasWebSerializer