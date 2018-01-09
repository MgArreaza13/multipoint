from django.conf.urls import url
from django.contrib import admin

#ingresos
from apps.Inflacion.views import NuevoRegistroDeInflacion
from apps.Inflacion.views import EditarReistroDeInflacion
from apps.Inflacion.views import EliminarRegistroDeInflacion

from apps.Inflacion.views import reajuste



urlpatterns = [

	#url(r'^$', Configuracion , name='Configuracion'  ),
	#Turnos 
	url(r'^Nuevo/Registro/$', NuevoRegistroDeInflacion , name='NuevoRegistroDeInflacion'  ),
	url(r'^Registro/Editar/(?P<id_registro>\d+)$', EditarReistroDeInflacion, name='EditarReistroDeInflacion'  ),
	url(r'^Registro/Borrar/(?P<id_registro>\d+)$', EliminarRegistroDeInflacion, name='EliminarRegistroDeInflacion'  ),
	url(r'^Registro/consulta/inflacion/$', reajuste, name='reajuste'  ),
	#url(r'^Perfil/(?P<id_Client>\d+)$', ClienteProfile , name='ClienteProfile'  ),
	#url(r'^list/$', ListProductos , name='ListProductos'  ),
 
]