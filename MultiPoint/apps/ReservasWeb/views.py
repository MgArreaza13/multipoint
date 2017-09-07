from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from apps.ReservasWeb.models import tb_reservasWeb
#Modelos 
from apps.Turn.models import tb_turn
from apps.Collaborator.models import tb_collaborator
from apps.Turn.models import tb_turn
from apps.Caja.models import tb_ingreso
from apps.Caja.models import tb_egreso
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



@login_required(login_url = 'Demo:login' )
def listReservas(request):
	TurnEditar = -1 #para poder saber que turnos se le mostrara el formulario, verifico que ningun id coincida con -1
	reservas = tb_reservasWeb.objects.all()
	result = validatePerfil(tb_profile.objects.filter(user=request.user))
	perfil = result[0]
	formulario = False
	#queryset 
	turnos_hoy =  tb_turn.objects.filter(dateTurn=date.today()).filter(statusTurn__nameStatus='En Espera').count()
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
			reserva.telefono = ReservaWebEditar.telefono
			reserva.save()
			return redirect ('Reservas:listReservas')
	return render (request, 'ReservasWeb/listaDeReservas.html', {'ReservaWebEditar':ReservaWebEditar,'reservas':reservas,'Form':Form , 'perfil':perfil})

def web(request):
	turnos = tb_turn.objects.filter(statusTurn__nameStatus="En Espera")
	Form = ReservasWebForm
	fallido = None
	if request.method == 'POST':
		Form = ReservasWebForm(request.POST or None)
		if Form.is_valid():
			turno = Form.save(commit=False)
			turno.dateTurn = request.POST['TurnDate']
			turno.HoraTurn = request.POST['TimeTurn']
			turno.statusTurn = tb_status.objects.get(nameStatus="Sin Aprobar")
			turno.save()
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
			return render(request, "ReservasWeb/reservasweb.html" , {'Form':Form ,'turnos':turnos ,'mensaje':mensaje,})
		else:
				fallido = "Errores en los datos Verifiquelos, y vuelva a intentarlo"
				Form = ReservasWebForm()
	return render(request, "ReservasWeb/reservasweb.html" , {'Form':Form ,'turnos':turnos ,'fallido':fallido,})




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