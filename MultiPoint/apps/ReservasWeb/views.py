from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from datetime import date
#Modelos 
from apps.Turn.models import tb_turn
from apps.Collaborator.models import tb_collaborator
from apps.Turn.models import tb_turn
from apps.Caja.models import tb_ingreso
from apps.Caja.models import tb_egreso
#FORMULARIOS
from apps.ReservasWeb.forms import ReservasWebForm
from apps.Turn.forms import EditTurnForm
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
			email_body_Soporte = "se ha registrado una nueva reserva , nombre:%s . correo:%s, numero:%s , te invitamos a contactarla y luego a cambiar el status de la reserva en  http://multipoint.pythonanywhere.com/" %(turno.nombre, turno.mail, turno.telefono)
			message_Soporte = (email_subject_Soporte, email_body_Soporte , 'as.estiloonline@gmail.com', ['soporte@apreciasoft.com', "mg.arreaza.13@gmail.com"])
			#enviamos el correo
			send_mass_mail((message_usuario, message_Soporte), fail_silently=False)
			return render(request, "ReservasWeb/reservasweb.html" , {'Form':Form ,'turnos':turnos ,'mensaje':mensaje,})
		else:
				fallido = "Errores en los datos Verifiquelos, y vuelva a intentarlo"
				Form = ReservasWebForm()
	return render(request, "ReservasWeb/reservasweb.html" , {'Form':Form ,'turnos':turnos ,'fallido':fallido,})