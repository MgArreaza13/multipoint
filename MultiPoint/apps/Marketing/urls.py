from django.conf.urls import url
from django.contrib import admin

#ingresos
from apps.Marketing.views import VistaPrincipal
from apps.Marketing.views import NuevoCorreo
from apps.Marketing.views import enviarMasivamenteCorreo
from apps.Marketing.views import ObtenerMail
#from apps.Inflacion.views import EditarReistroDeInflacion
#from apps.Inflacion.views import EliminarRegistroDeInflacion

#from apps.Inflacion.views import reajuste



urlpatterns = [

	url(r'^$', VistaPrincipal , name='VistaPrincipal'  ),
	url(r'^Nuevo/Correo/', NuevoCorreo , name='NuevoCorreo'  ),
	#Turnos 
	url(r'^Nuevo/Envio/de/correo/masivo$', enviarMasivamenteCorreo , name='enviarMasivamenteCorreo'  ),
	url(r'^Correo/(?P<id_mail>\d+)$', ObtenerMail, name='ObtenerMail'  ),
	#url(r'^Registro/Borrar/(?P<id_registro>\d+)$', EliminarRegistroDeInflacion, name='EliminarRegistroDeInflacion'  ),
	#url(r'^Registro/consulta/inflacion/$', reajuste, name='reajuste'  ),
	#url(r'^Perfil/(?P<id_Client>\d+)$', ClienteProfile , name='ClienteProfile'  ),
	#url(r'^list/$', ListProductos , name='ListProductos'  ),
 
]