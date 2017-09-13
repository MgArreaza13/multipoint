from django.db import models
from apps.Configuracion.models import tb_status
from apps.Service.models import tb_service

# Create your models here.
class tb_reservasWeb (models.Model):
	servicioPrestar			= 	models.ForeignKey(tb_service,on_delete=models.CASCADE, null=False, default='')
	dateTurn				=	models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False, default='')
	HoraTurn				=	models.TimeField(auto_now=False, auto_now_add=False, blank=False, null=False, default='')
	mail					=  	models.EmailField(default='', null=False, max_length=30)
	nombre					= 	models.CharField(default='', null=False, max_length=30)
	telefono				=	models.CharField(default='', null=False, max_length=30)
	statusTurn 				=	models.ForeignKey(tb_status, on_delete=models.CASCADE, null=False, default='')
	def __str__(self):
		return self.mail