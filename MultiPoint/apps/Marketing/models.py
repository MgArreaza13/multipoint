from django.db import models
from django.conf import settings
# Create your models here.


class tb_mail (models.Model):
	user					=	models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, default='')
	#dni						=	models.IntegerField(default='', null=False)
	Asunto					=	models.CharField(default='Multipoint - Eventos', null=True, max_length=30000)
	Mailbody				=	models.TextField(default='', null=True, max_length=30000)
	#addressClient 			=	models.TextField(default='', null=False)
	#CollaboratorFavoriteKf	= 	models.ForeignKey(tb_collaborator, on_delete=models.CASCADE, null=False, default='')
	#addressClientTwo		= 	models.TextField(default='', null=False)
	#isSendPromotions		=	models.BooleanField()
	dateCreate				=	models.DateField(auto_now=True, blank=False)
	#isVip					= 	models.BooleanField()
	#StatusKf				=	models.ForeignKey(tb_status_turn, on_delete=models.CASCADE, null=False, default='')
	#TypeClienteKf			=	models.ForeignKey(tb_type_client, on_delete=models.CASCADE, null=False, default='')
	def __str__(self):
		return self.Asunto