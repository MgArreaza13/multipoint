from django.conf.urls import url
from django.contrib import admin
from apps.Turn.views import listTurnos
from apps.Turn.views import NuevoTurn
from apps.Turn.views import NuevoTurnParaHoy
from apps.Turn.views import EditTurnStatus
from apps.Turn.views import EditTurn
from apps.Turn.views import DeleteTurn
from apps.Turn.views import index
from apps.Turn.views import EditTurnList
from apps.Turn.views import NuevoTurnClient
from apps.Turn.views import ReservaWebPanelPorPagar
from apps.Turn.views import FacturaTurn
from apps.Turn.views import TurnPago
from apps.Turn.views import TurnStatus
from apps.Turn.views import TurnStatusChange
from apps.Turn.views import DetallesTurn



urlpatterns = [

	url(r'^$', index , name='index'  ),
	#url(r'^Perfil/(?P<id_Client>\d+)$', ClienteProfile , name='ClienteProfile'  ),
	url(r'^list/$', listTurnos , name='listTurnos'  ),
	url(r'^list/Status/(?P<id_turn>\d+)$', EditTurnList , name='EditTurnList'  ),
	url(r'^Nuevo/(?P<id_client>\d+)$', NuevoTurnClient , name='NuevoTurnClient'  ),
	url(r'^detalles/(?P<id_turn>\d+)$', DetallesTurn , name='DetallesTurn'  ),
	url(r'^Nuevo/Hoy$', NuevoTurnParaHoy , name='NuevoTurnParaHoy'  ),
	url(r'^Nuevo/$', NuevoTurn , name='NuevoTurn'  ),
	url(r'^Actualizar/Status/(?P<id_turn>\d+)$', EditTurnStatus, name='EditTurnStatus'  ),
	url(r'^Editar/(?P<id_turn>\d+)$', EditTurn, name='EditTurn'  ),
	url(r'^Borrar/(?P<id_turn>\d+)$', DeleteTurn, name='DeleteTurn'  ),
	url(r'^Pagar/(?P<id_reserva>\d+)$', ReservaWebPanelPorPagar, name='ReservaWebPanelPorPagar'  ),
	url(r'^Factura/(?P<id_turn>\d+)$', FacturaTurn, name='FacturaTurn'  ),
  	url(r'^Procesar/Pago/(?P<id_turn>\d+)$', TurnPago, name='TurnPago'  ),
	url(r'^Procesar/Pago/Status$', TurnStatus, name='TurnStatus'  ),
	url(r'^Procesar/Pago/Status/change$', TurnStatusChange, name='TurnStatusChange'  ),


]