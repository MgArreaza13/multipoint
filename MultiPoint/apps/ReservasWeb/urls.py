from django.conf.urls import url
from django.contrib import admin
#from apps.Proveedores.views import Servicios
from apps.ReservasWeb.views import web
from apps.ReservasWeb.views import listReservas
from apps.ReservasWeb.views import EditReservaList
from apps.ReservasWeb.views import DeleteReservas
from apps.ReservasWeb.views import Factura
from apps.ReservasWeb.views import validacion
from apps.ReservasWeb.views import ReservaWebPorPagar
from apps.ReservasWeb.views import Pago
from apps.ReservasWeb.views import Status
from apps.ReservasWeb.views import StatusChange
from apps.ReservasWeb.views import returnPago
from apps.ReservasWeb.views import CorreoDePagoSucursal




urlpatterns = [

	#url(r'^$', Servicios , name='Servicios'  ),
	#url(r'^Perfil/(?P<id_Client>\d+)$', ClienteProfile , name='ClienteProfile'  ),
	url(r'^web/$', web , name='web'  ),
	url(r'^ajax/validacion/$', validacion , name='validacion'  ),
	url(r'^factura/(?P<id_reservas>\d+)$', Factura , name='Factura'  ),
	url(r'^list/$', listReservas , name='listReservas'  ),
	#url(r'^Nuevo/$', NuevoProveedor , name='NuevoProveedor'  ),
	url(r'^Editar/(?P<id_reservas>\d+)$', EditReservaList, name='EditReservaList'  ),
	url(r'^Borrar/(?P<id_reservas>\d+)$', DeleteReservas, name='DeleteReservas'  ),
	url(r'^Pagar/(?P<id_reserva>\d+)$', ReservaWebPorPagar, name='ReservaWebPorPagar'  ),
 	url(r'^Procesar/Pago/(?P<id_reserva>\d+)$', Pago, name='Pago'  ),
	url(r'^Procesar/Pago/Status$', Status, name='Status'  ),
	url(r'^Procesar/Pago/Status/change$', StatusChange, name='StatusChange'  ),
	url(r'^Procesar/Pago/Status/Retorno$', returnPago, name='returnPago'  ),
	url(r'^Correo/Pago/Sucursal$', CorreoDePagoSucursal, name='CorreoDePagoSucursal'  ),

]