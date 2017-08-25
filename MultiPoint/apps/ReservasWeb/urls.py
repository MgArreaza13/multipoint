from django.conf.urls import url
from django.contrib import admin
#from apps.Proveedores.views import Servicios
from apps.ReservasWeb.views import web



urlpatterns = [

	#url(r'^$', Servicios , name='Servicios'  ),
	#url(r'^Perfil/(?P<id_Client>\d+)$', ClienteProfile , name='ClienteProfile'  ),
	url(r'^web/$', web , name='web'  ),
	#url(r'^Nuevo/$', NuevoProveedor , name='NuevoProveedor'  ),
	#url(r'^Editar/(?P<id_proveedor>\d+)$', EditarProveedor, name='EditarProveedor'  ),
	#url(r'^Borrar/(?P<id_proveedor>\d+)$', EliminarProveedor, name='EliminarProveedor'  ),
  
]