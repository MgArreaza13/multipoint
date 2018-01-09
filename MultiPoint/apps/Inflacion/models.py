from django.db import models
from django.conf import settings
# Create your models here.


class tb_inflacion (models.Model):
	user 								=	models.ForeignKey(settings.AUTH_USER_MODEL)
	Enero								=	models.IntegerField(default='', null=True)
	Febrero								=	models.IntegerField(default='', null=True)
	Marzo								=	models.IntegerField(default='', null=True)
	Abril								=	models.IntegerField(default='', null=True)
	Mayo								=	models.IntegerField(default='', null=True)
	Junio								=	models.IntegerField(default='', null=True)
	Julio								=	models.IntegerField(default='', null=True)
	Agosto								=	models.IntegerField(default='', null=True)
	Septiembre							=	models.IntegerField(default='', null=True)
	Octubre								=	models.IntegerField(default='', null=True)
	Noviembre							=	models.IntegerField(default='', null=True)
	Diciembre							=	models.IntegerField(default='', null=True)
	#CollaboratorFavoriteKf		= 	models.ForeignKey(tb_collaborator, on_delete=models.CASCADE, null=False, default='')
	#addressProveedorTwo			= 	models.TextField(default='', null=False)
	#isSendPromotions			=	models.BooleanField()
	dateCreate					=	models.DateField(auto_now=True, blank=False)
	#isVip						= 	models.BooleanField()
	#StatusKf					=	models.ForeignKey(tb_status_turn, on_delete=models.CASCADE, null=False, default='')
	#TypeClienteKf				=	models.ForeignKey(tb_type_client, on_delete=models.CASCADE, null=False, default='')
	