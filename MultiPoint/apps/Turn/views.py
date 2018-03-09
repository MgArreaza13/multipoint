from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from django.http import JsonResponse
#Modelos 
from django.http import HttpResponse
from apps.Turn.models import tb_turn
from apps.Collaborator.models import tb_collaborator
from apps.Turn.models import tb_turn
from apps.Caja.models import tb_ingreso
from apps.Caja.models import tb_egreso
from apps.ReservasWeb.models import tb_reservasWeb
from apps.Client.models import tb_client
from apps.Configuracion.models import tb_status

from apps.Configuracion.models import tb_formasDePago
from apps.Configuracion.models import tb_tipoIngreso
#FORMULARIOS
from apps.Turn.forms import TurnForm
from apps.Turn.forms import EditTurnForm
from apps.Turn.forms import TurnFormClient
#datos para la vista principal arriba de las citas y los ingresos.
from django.db.models import Count, Min, Sum, Avg
from datetime import date 
# Create your views here.
from apps.UserProfile.models import tb_profile
from apps.scripts.validatePerfil import validatePerfil
# enviar correos
from django.core.mail import send_mail
from django.core.mail import send_mass_mail

from apps.Service.models import tb_service
from apps.Product.models import tb_product
from apps.Notificaciones.models import Notificacion

from apps.Caja.forms import WebReservasIngresoForm
from apps.scripts.SumarHora import sumar_hora


from ingenico.connect.sdk.factory import Factory
from apps.ingenico.MycheckoutSupport import Pago_Online
from apps.ingenico.MycheckoutSupport import statusDePago
from apps.Configuracion.models import tb_logo

from apps.Configuracion.models import tb_turn_sesion
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
from apps.Client.models import tb_client_WEB
from apps.Configuracion.models import tb_logo
from apps.Configuracion.models import tb_turn_sesion
from django.core import serializers
from apps.Configuracion.models import tb_turn_sesion




@login_required(login_url = 'Demo:login' )
def DetallesTurn(request, id_turn):
	reserva = tb_turn.objects.get(id=id_turn)
	fecha = date.today()
	admin = tb_profile.objects.filter(tipoUser='Administrador')
	administrador = admin[0]
	logo = tb_logo.objects.get(id=1)

	
	return render(request, 'Turn/DetallesTurn.html', {'reserva':reserva,'logo':logo, 'administrador':administrador ,'fecha':fecha})


def FacturaTurn(request, id_turn):
	reserva = tb_turn.objects.get(id=id_turn)
	fecha = date.today()
	admin = tb_profile.objects.filter(tipoUser='Administrador')
	administrador = admin[0]

	
	return render(request, 'Turn/Confirmacionturn.html', {'reserva':reserva,'administrador':administrador ,'fecha':fecha})



def TurnPago(request, id_turn):
	reserva = tb_turn.objects.get(id=id_turn)
	data = Pago_Online(reserva.montoAPagar)
	url = "https://payment."+data._CreateHostedCheckoutResponse__partial_redirect_url

	reserva.ingenico_id =data._CreateHostedCheckoutResponse__hosted_checkout_id
	
	reserva.save()
	return redirect(url)


def TurnStatus(request):
	pk = request.GET.get('pk', None)
	
	reserva = tb_turn.objects.get(id= pk)
	status = (statusDePago(reserva.ingenico_id))
	data = {
        'status':status._GetHostedCheckoutResponse__status
    }
	return JsonResponse(data)


def TurnStatusChange(request ):
	pk = request.GET.get('pk', None)
	reserva = tb_turn.objects.get(id= pk)
	reserva.isPay = True
	reserva.statusTurn =  tb_status.objects.get(nameStatus= 'Confirmada') 
	reserva.PagoOnline = True
	reserva.save()
	request.session['user'] = reserva.nombre
	#creamos el ingreso 
	ingreso = tb_ingreso()
	ingreso.user = request.session['user']
	ingreso.tipoPago = tb_formasDePago.objects.get(nameFormasDePago='Pago Online')
	ingreso.tipoIngreso = tb_tipoIngreso.objects.get(nameTipoIngreso='Servicios Web')
	ingreso.service = reserva.servicioPrestar
	ingreso.monto = reserva.montoAPagar
	ingreso.descripcion = 'Pagado desde el Motor de Pagos Online'
	ingreso.save()
	#mandar correo cuando se paga la reserva
	usuario = reserva.client.user.mailUser #trato de traer el colaborador del formulario
	email_subject_usuario = 'Multipoint - Gracias Por su Pago'
	email_body_usuario = "Hola %s, gracias por completar su pago de manera exitosa, hemos aprobado su solicitud ya de servicio , esperemos disfrute nuestros servicios" %(reserva.client)
	message_usuario = (email_subject_usuario, email_body_usuario , 'eventos@b7000615.ferozo.com', [usuario])
	#mensaje para apreciasoft
	email_subject_Soporte = 'Multipoint - Nueva Reserva WEB PAGADA'
	email_body_Soporte = "se ha registrado un Pago de una  reserva , nombre:%s . correo:%s, numero:%s , para un servicio %s, y un monto de $%s te invitamos a revisarla en http://179.43.123.41:8000/reservas/list/" %(reserva.client, reserva.client.user.mailUser, reserva.client.phoneNumberClient, reserva.servicioPrestar, reserva.montoAPagar)
	message_Soporte = (email_subject_Soporte, email_body_Soporte , 'eventos@b7000615.ferozo.com', ['soporte@apreciasoft.com', "mg.arreaza.13@gmail.com", 'reservas@boomeventos.com', ])
	#enviamos el correo
	send_mass_mail((message_usuario, message_Soporte), fail_silently=False)
	
	return HttpResponse('ok')







#Resumen de todos los turnos, parte principal
@login_required(login_url = 'Demo:login' )
def index(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	fecha =  date.today()
	TurnEditar = -1 #para poder saber que turnos se le mostrara el formulario, verifico que ningun id coincida con -1
	is_collaborador = tb_collaborator.objects.filter(user__id = request.user.id) #saber si el usuario actual es collaborador
	turnos = tb_turn.objects.filter(dateTurn = fecha)
	reservas = tb_reservasWeb.objects.filter(dateTurn = fecha)
	#queryset 
	reservas_hoy = tb_reservasWeb.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='Confirmada').count()
	turnos__hoy =  tb_turn.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='Confirmada').count()
	turnos_hoy = reservas_hoy + turnos__hoy
	ingresos_hoy = tb_ingreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	egresos_hoy  = tb_egreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	context = {
	'reservas':reservas,
	'perfil':perfil,
	'is_collaborador':is_collaborador,
	'turnos':turnos,
	'fecha':fecha, 
	'turnos_hoy':turnos_hoy,
	'ingresos_hoy':ingresos_hoy,
	'egresos_hoy':egresos_hoy,
	'TurnEditar':TurnEditar

	}
	return render(request,'Turn/ResumenTurnos.html', context )




@login_required(login_url = 'Demo:login' )
def ReservaWebPanelPorPagar(request, id_reserva):
	reserva = tb_turn.objects.get(id=id_reserva)
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
			ingreso.descripcion = "Pago de Reserva Web Desde el Panel"
			ingreso.service = reserva.servicioPrestar
			ingreso.monto = reserva.montoAPagar
			ingreso.save()
			reserva.isPay = True
			reserva.save()
			mensaje = "Gracias Por registrar Su Pago"
			usuario = reserva.client.user.mailUser #trato de traer el colaborador del formulario
			email_subject_usuario = 'Multipoint - Gracias Por su Pago'
			email_body_usuario = "Hola %s, gracias por completar su pago de manera exitosa, esperemos disfrute nuestros servicios" %(reserva.client)
			message_usuario = (email_subject_usuario, email_body_usuario , 'eventos@b7000615.ferozo.com', [usuario])
			#mensaje para apreciasoft
			email_subject_Soporte = 'Multipoint - Nueva Reserva WEB PAGADA'
			email_body_Soporte = "se ha registrado un Pago de una  reserva , nombre:%s . correo:%s, numero:%s , te invitamos a contactarla y luego a cambiar el status de la reserva en  http://179.43.123.41:8000/reservas/list/" %(reserva.client, reserva.client.user.mailUser, reserva.client.phoneNumberClient)
			message_Soporte = (email_subject_Soporte, email_body_Soporte , 'eventos@b7000615.ferozo.com', ['soporte@apreciasoft.com', "mg.arreaza.13@gmail.com", 'reservas@boomeventos.com', ])
			#enviamos el correo
			send_mass_mail((message_usuario, message_Soporte), fail_silently=False)
			return render(request, 'Turn/FacturaPorPagarPanel.html' , {'Form':Form, 'perfil':perfil, 'mensaje':mensaje, 'reserva':reserva,'administrador':administrador,'fecha':fecha,})
		else: 
			Form = WebReservasIngresoForm()
			fallido = "Hemos tenido algun problema con sus datos, por eso no hemos procesado su ingreso, verifiquelo e intentelo de nuevo"
			
	return render(request , 'Turn/FacturaPorPagarPanel.html' , {'fallido':fallido,
			'Form':Form,
			'reserva':reserva,
			'administrador':administrador,
			'fecha':fecha,})




#crea los turnos
@login_required(login_url = 'Demo:login' )
def NuevoTurnClient(request , id_client):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	turnos = tb_turn.objects.filter(statusTurn__nameStatus="Confirmada")
	ReservasWeb = tb_reservasWeb.objects.filter(statusTurn__nameStatus="Confirmada")
	servicios = tb_service.objects.all()
	productos = tb_product.objects.all()
	tipe_turnos = tb_turn_sesion.objects.all()
	perfil = result[0]
	Form = TurnFormClient
	mensaje1 = None
	fallido = None
	notificacion = Notificacion()
	if request.method == 'POST':
		Form = TurnFormClient(request.POST or None)
		#ReservaWebOcupada = tb_turn.objects.filter(dateTurn=request.POST['TurnDate']).filter(statusTurn__nameStatus="Confirmada").filter(HoraTurn=request.POST['TimeTurn'])	
		#data = len(ReservaWebOcupada)
		if Form.is_valid():
			#if data == 0: #no encontro un collaborador ocupado para ese dia y hora 
			turno = Form.save(commit=False)

			turno.user = request.user
			turno.dateTurn = request.POST['FechaSeleccionada']
			turno.client = tb_client.objects.get(user__user__id = request.user.id)
			turno.turn = tb_turn_sesion.objects.get(id=request.POST['TurnSeleccionado'])
			turno.statusTurn = tb_status.objects.get(nameStatus="Sin Aprobar")
			turno.extraInfoTurn = 'Sin Comentarios'
			turno.servicioPrestar = tb_service.objects.get(id= request.POST['ServicioSeleccionado'])
			turno.montoAPagar = float(request.POST['total'])  
			turno.statusTurn = tb_status.objects.get(nameStatus='Sin Aprobar')
			turno.save()
			notificacion.nombre = turno.client.user.nameUser
			notificacion.dateTurn = turno.dateTurn
			notificacion.save()
				#Enviaremos los correos a el colaborador y al cliente 
				#colaborador
				#colaborador = tb_profile.objects.get(nameUser=turno.collaborator) #trato de traer el colaborador del formulario
				#email_subject_Colaborador = 'Nuevo Turno Solicitado Por Cliente'
				#email_body_Colaborador = "Hola %s, El presente mensaje es para informarle que ha recibido una nueva solicitud para un turno si desea revisarla y confirmarla ingrese aqui http://179.43.123.41:8000/" %(colaborador)
				#email_colaborador = colaborador.mailUser
				#message_colaborador = (email_subject_Colaborador, email_body_Colaborador , 'eventos@b7000615.ferozo.com', [email_colaborador])
				#cliente
			client = tb_profile.objects.get(user__username=turno.client) #trato de traer el colaborador del formulario
			email_subject_client = 'Nuevo Turno Solicitado'
			email_body_Client = "Hola %s, El presente mensaje es para informarle que se ha enviado una nueva solicitud para un turno ya nos pondremos en contacto con usted" %(client)
			email_client = client.mailUser
			message_client = (email_subject_client, email_body_Client, 'eventos@b7000615.ferozo.com', [email_client])
				#mensaje para apreciasoft
			email_subject_Soporte = 'Nuevo Turno Solicitado en Estilo Online'
			email_body_Soporte = "Hola, El presente mensaje es para informarle que el cliente  %s ha enviado una nueva solicitud para de reserva , si desea revisarla ingrese aqui http://179.43.123.41:8000/" %(client)
			message_Soporte = (email_subject_Soporte, email_body_Soporte , 'eventos@b7000615.ferozo.com', ['soporte@apreciasoft.com', 'mg.arreaza.13@gmail.com', 'reservas@boomeventos.com', ])
				#enviamos el correo
			send_mass_mail(( message_client, message_Soporte), fail_silently=False)
			mensaje = "Hemos Guardado sus datos de manera correcta"
			return redirect('Turnos:FacturaTurn', id_turn=turno.id)
		else:
				mensaje1 = "Errores en los datos Verifiquelos, y vuelva a intentarlo"
				Form = TurnFormClient()
				fallido = "Tuvimos un error al cargar sus datos, verifiquelo e intente de nuevo"
	return render(request, 'Turn/NuevoTurno.html' , {'Form':Form, 'tipe_turnos':tipe_turnos ,'servicios':servicios, 'productos':productos  ,'ReservasWeb':ReservasWeb ,'turnos':turnos ,'mensaje1':mensaje1, 'perfil':perfil, 'fallido':fallido})







#Crea El turno para la fecha actual
@login_required(login_url = 'Demo:login' )
def NuevoTurnParaHoy(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	turnos = tb_turn.objects.filter(statusTurn__nameStatus="Confirmada")
	ReservasWeb = tb_reservasWeb.objects.filter(statusTurn__nameStatus="Confirmada")
	perfil = result[0]
	Form = TurnForm
	fecha =  date.today()
	servicios = tb_service.objects.all()
	productos = tb_product.objects.all()
	tipe_turnos = tb_turn_sesion.objects.all()
	mensaje1 = None
	fallido = None
	notificacion = Notificacion()
	if request.method == 'POST':
		Form = TurnForm(request.POST or None)
		fecha =  date.today()
		#ReservaWebOcupada = tb_turn.objects.filter(dateTurn=fecha).filter(statusTurn__nameStatus="Confirmada").filter(HoraTurn=request.POST['TimeTurn'])
		#data = len(ReservaWebOcupada)
		if Form.is_valid():
			turno = Form.save(commit=False)
			turno.user = request.user
			turno.dateTurn = fecha
			turno.turn = tb_turn_sesion.objects.get(id=request.POST['TurnSeleccionado'])
			turno.statusTurn = tb_status.objects.get(nameStatus="Sin Aprobar")
			turno.extraInfoTurn = 'Sin Comentarios'
			turno.TipoReservas = "RESERVA"
				#Envio de mensajes 
				#colaborador = tb_profile.objects.get(nameUser=turno.collaborator) #trato de traer el colaborador del formulario
				#email_subject_Colaborador = 'Nuevo Turno Solicitado Por Cliente'
				#email_body_Colaborador = "Hola %s, El presente mensaje es para informarle que ha recibido una nueva solicitud para un turno si desea revisarla y confirmarla ingrese aqui http://179.43.123.41:8000/" %(colaborador)
				#email_colaborador = colaborador.mailUser
				#message_colaborador = (email_subject_Colaborador, email_body_Colaborador , 'eventos@b7000615.ferozo.com', [email_colaborador])
				#cliente
			if request.POST['ServicioSeleccionado'] != 'None':
				turno.servicioPrestar=tb_service.objects.get(id = request.POST['ServicioSeleccionado'])
			turno.montoAPagar = float(request.POST['total'])  
			turno.save()
			notificacion.nombre = turno.client.user.nameUser
			notificacion.dateTurn = turno.dateTurn
			notificacion.save()
			client = tb_profile.objects.get(user__username=turno.client) #trato de traer el colaborador del formulario
			email_subject_client = 'Nuevo Turno Solicitado'
			email_body_Client = "Hola %s, El presente mensaje es para informarle que se ha enviado una nueva solicitud para un turno ya nos pondremos en contacto con usted , gracias" %(client)
			email_client = client.mailUser
			message_client = (email_subject_client, email_body_Client, 'eventos@b7000615.ferozo.com', [email_client])
				#mensaje para apreciasoft
			email_subject_Soporte = 'Nuevo Turno Solicitado en Estilo Online'
			email_body_Soporte = "Hola, soporte Apreciasoftit, El presente mensaje es para informarle que el cliente  %s ha enviado una nueva solicitud de Reservas , si desea revisarla ingrese aqui http://179.43.123.41:8000/" %(client)
			message_Soporte = (email_subject_Soporte, email_body_Soporte , 'eventos@b7000615.ferozo.com', ['soporte@apreciasoft.com', 'reservas@boomeventos.com', 'mg.arreaza.13@gmail.com'])
				#enviamos el correo
			send_mass_mail((message_client, message_Soporte), fail_silently=False)
				
			mensaje = 'Felicidades Hemos podido guardar su turno de manera exitosa'
			return redirect('Turnos:FacturaTurn', id_turn=turno.id)
		else:
			mensaje = "Errores en los datos Verifiquelos, y vuelva a intentarlo"
			fecha =  date.today()
			Form = TurnForm()
			fallido = "No hemos podido cargar sus datos correctamente, verifique e intente nuevamente"

	
	return render(request, 'Turn/NuevoTurnoHoy.html' , {'Form':Form, 'tb_turn_sesion':tb_turn_sesion ,'servicios':servicios, 'productos':productos ,'ReservasWeb':ReservasWeb,'turnos':turnos ,'fecha':fecha , 'mensaje1':mensaje1, 'perfil':perfil, 'fallido':fallido})


#Edita los Status de los turnos
@login_required(login_url = 'Demo:login' )
def EditTurnStatus(request , id_turn):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	tipo = 'TURNO'
	Reservas = tb_reservasWeb.objects.exclude(statusTurn__nameStatus='Sin Aprobar').order_by('dateTurn')
	turnos = tb_turn.objects.filter(dateTurn = date.today())
	TurnEditar = tb_turn.objects.get(id = id_turn)
	fallido = None
	if request.method == 'GET':
		Form= EditTurnForm(instance=TurnEditar)
	else:
		Form= EditTurnForm(request.POST,instance=TurnEditar)
		if  Form.is_valid():
			turno 		 = Form.save(commit=False)
			turno.user	 = request.user
			turno.dateTurn = TurnEditar.dateTurn
			turno.turn = TurnEditar.turn
			turno.client = TurnEditar.client
			turno.extraInfoTurn = TurnEditar.extraInfoTurn
			turno.servicioPrestar = TurnEditar.servicioPrestar
			turno.isPay = TurnEditar.isPay
			turno.save()
			mensaje = "hemos cargado sus nuevos datos de manera exitosa"
			return render (request, 'Turn/ResumenTurnos.html', {'turnos':turnos,'Form':Form,'tipo':tipo, 'Reservas':Reservas, 'TurnEditar':TurnEditar, 'perfil':perfil, 'mensaje':mensaje})
	return render (request, 'Turn/ResumenTurnos.html', {'turnos':turnos,'Form':Form,'tipo':tipo, 'Reservas':Reservas, 'TurnEditar':TurnEditar, 'perfil':perfil, 'fallido':fallido})


#lista todo los turnos en la tabla
@login_required(login_url = 'Demo:login' )
def listTurnos(request):
	formas_de_pago = tb_formasDePago.objects.all()
	TurnEditar = -1 #para poder saber que turnos se le mostrara el formulario, verifico que ningun id coincida con -1
	turnos = tb_turn.objects.all().order_by('dateTurn')
	Reservas = tb_reservasWeb.objects.exclude(statusTurn__nameStatus='Sin Aprobar').order_by('dateTurn')
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	formulario = False
	status = tb_status.objects.all()
	#queryset 
	reservas_hoy = tb_reservasWeb.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='Confirmada').count()
	turnos__hoy =  tb_turn.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='Confirmada').count()
	turnos_hoy = reservas_hoy + turnos__hoy
	ingresos_hoy = tb_ingreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	egresos_hoy  = tb_egreso.objects.filter(dateCreate=date.today()).aggregate(total=Sum('monto'))
	context = {
	'status':status,
	'formas_de_pago':formas_de_pago,
	'Reservas':Reservas,
	'perfil':perfil,
	'turnos':turnos,
	'turnos_hoy':turnos_hoy,
	'ingresos_hoy':ingresos_hoy,
	'egresos_hoy':egresos_hoy,
	'TurnEditar':TurnEditar,

	}
	return render(request,'Turn/ListaDeTurnos.html',context )

#crea los turnos
@login_required(login_url = 'Demo:login' )
def NuevoTurn(request):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	turnos = tb_turn.objects.filter(statusTurn__nameStatus="Confirmada")
	ReservasWeb = tb_reservasWeb.objects.filter(statusTurn__nameStatus="Confirmada")
	productos = tb_product.objects.all()
	servicios = tb_service.objects.all()
	Form = ReservasWebForm
	notificacion = Notificacion()
	tipe_turnos = tb_turn_sesion.objects.all()
	perfil = result[0]

	user = tb_client_WEB()
	fallido = None
	if request.method == 'POST':
		Form = ReservasWebForm(request.POST or None)
		if Form.is_valid():
			print(request.POST)
			turno = Form.save(commit=False)
			turno.dateTurn = request.POST['FechaSeleccionada']
			turno.turn = tb_turn_sesion.objects.get(id=request.POST['TurnSeleccionado'])
			turno.statusTurn = tb_status.objects.get(nameStatus="Sin Aprobar")
			if request.POST['ServicioSeleccionado'] != 'None':
				turno.servicioPrestar=tb_product.objects.get(id = request.POST['ServicioSeleccionado'])
			turno.montoAPagar = float(request.POST['total'])  
			turno.TipoReservas = "RESERVA"
			if request.POST['observaciones'] != '':
				turno.observaciones = request.POST['observaciones']
			if request.POST['ProductosSeleccionados'] != ' ':
				turno.description = request.POST['ProductosSeleccionados']
			else:
				turno.description = 'Sin Descripcion'
			print(turno.description)
			turno.save()
			notificacion.nombre = turno.nombre
			notificacion.dateTurn = turno.dateTurn
			notificacion.save()
			#creo el cliente web , debo validar si ya existe y agregar un contador
			query_set_user = tb_client_WEB.objects.filter(mail= turno.mail)
			if (len(query_set_user) == 1):
				print('entre en el condicional')
				query_set_user[0].numeroReservasWeb += 1
				query_set_user[0].save()
			else:
				user = tb_client_WEB()
				user.nombre = turno.nombre
				user.mail = turno.mail
				user.FormaDeRegistro = 'Registro Web' 
				user.telefono = turno.telefono
				user.save()

			turno_enviar = tb_reservasWeb.objects.get(id=turno.id)
			mensaje ="se ha registrado de forma correcta sus datos gracias por contactarnos"
			#mandar mensaje de nuevo usuario
			#Enviaremos los correos a el colaborador y al cliente 
			#cliente
			usuario = turno.mail #trato de traer el colaborador del formulario
			email_subject_usuario = 'Multipoint - Nueva Reserva'
			email_body_usuario = "Hola %s, gracias por solicitar una nueva reserva ya nos pondremos en contacto con usted , gracias" %(turno.nombre)
			message_usuario = (email_subject_usuario, email_body_usuario , 'eventos@b7000615.ferozo.com', [usuario])
			#mensaje para apreciasoft
			email_subject_Soporte = 'Multipoint - Nueva Reserva'
			email_body_Soporte = "se ha registrado una nueva reserva , nombre:%s . correo:%s, numero:%s , te invitamos a contactarla y luego a cambiar el status de la reserva en  http://179.43.123.41:8000/reservas/list/" %(turno.nombre, turno.mail, turno.telefono)
			message_Soporte = (email_subject_Soporte, email_body_Soporte , 'eventos@b7000615.ferozo.com', ['soporte@apreciasoft.com', "mg.arreaza.13@gmail.com", 'reservas@boomeventos.com',])
			#enviamos el correo
			#send_mass_mail((message_usuario, message_Soporte), fail_silently=False)
			return redirect('Reservas:Factura', id_reservas=turno.id)
		else:
				fallido = "Errores en los datos Verifiquelos, y vuelva a intentarlo"
				Form = ReservasWebForm()
	return render(request, 'Turn/NuevoTurno.html' , {'Form':Form, 'tipe_turnos':tipe_turnos ,'servicios':servicios,'productos':productos ,'ReservasWeb':ReservasWeb ,'turnos':turnos ,'fallido':fallido, 'perfil':perfil})

	

#edita los turnos en general
@login_required(login_url = 'Demo:login' )
def EditTurn(request , id_turn):
	TurnEditar = tb_turn.objects.get(id = id_turn)
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	turnos = tb_turn.objects.filter(statusTurn__nameStatus="Confirmada")
	ReservasWeb = tb_reservasWeb.objects.filter(statusTurn__nameStatus="Confirmada")
	tipe_turnos = tb_turn_sesion.objects.all()
	perfil = result[0]
	fallido = None
	if request.method == 'GET':
		Form= TurnForm(instance=TurnEditar)
	else:
		Form= TurnForm(request.POST,instance=TurnEditar)
		if  Form.is_valid():
			turno 		 = Form.save(commit=False)
			turno.user = request.user
			turno.dateTurn = request.POST['FechaSeleccionada']
			turno.turn = tb_turn_sesion.objects.get(id=request.POST['TurnSeleccionado'])
			turno.save()
			mensaje = "Guardamos sus datos de manera exitosa"
			return render (request, 'Turn/NuevoTurno.html', {'turnos':turnos,'Form':Form , 'perfil':perfil, 'mensaje':mensaje})
	return render (request, 'Turn/NuevoTurno.html', {'turnos':turnos, 'tb_turn_sesion':tb_turn_sesion ,'ReservasWeb':ReservasWeb ,'Form':Form , 'perfil':perfil, 'fallido':fallido})

#edita los turnos en general
@login_required(login_url = 'Demo:login' )
def EditTurnList(request , id_turn):
	formulario = True
	tipo = 'TURNO'
	turnos = tb_turn.objects.all().order_by('dateTurn')
	Reservas = tb_reservasWeb.objects.exclude(statusTurn__nameStatus='Sin Aprobar').order_by('dateTurn')
	TurnEditar = tb_turn.objects.get(id = id_turn)
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	if request.method == 'GET':
		idturn = id_turn
		Form= EditTurnForm(instance=TurnEditar)
	else:
		idturn = id_turn
		Form= EditTurnForm(request.POST,instance=TurnEditar)
		if  Form.is_valid():
			turno 		 = Form.save(commit=False)
			turno.user	 = request.user
			turno.dateTurn = TurnEditar.dateTurn
			turno.turn = TurnEditar.turn
			turno.client = TurnEditar.client
			turno.extraInfoTurn = TurnEditar.extraInfoTurn
			turno.servicioPrestar = TurnEditar.servicioPrestar
			turno.isPay = TurnEditar.isPay
			turno.save()
			return redirect ('Turnos:listTurnos')
	return render (request, 'Turn/ListaDeTurnos.html', {'TurnEditar':TurnEditar,'tipo':tipo ,'Reservas':Reservas,'turnos':turnos,'Form':Form , 'perfil':perfil})




#borra los turnos
@login_required(login_url = 'Demo:login' )
def DeleteTurn(request , id_turn):
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	TurnoBorrar = tb_turn.objects.get(id = id_turn)
	if request.method == 'POST':
		TurnoBorrar.delete()
		mensaje = "hemos borrado sus datos de manera exitosa"
		return render (request, 'Turn/DeleteTurno.html', {'TurnoBorrar':TurnoBorrar, 'perfil':perfil, 'mensaje':mensaje})
	return render (request, 'Turn/DeleteTurno.html', {'TurnoBorrar':TurnoBorrar, 'perfil':perfil})




from rest_framework import viewsets
from apps.Turn.serializers import turnSerializer

class TurnViewsets(viewsets.ModelViewSet):
	queryset = tb_turn.objects.all()
	serializer_class = turnSerializer