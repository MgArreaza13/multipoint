from django import forms
from django.forms import ModelForm, Textarea ,Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.ReservasWeb.models import tb_reservasWeb
from django.forms import extras



class ReservasWebForm(forms.ModelForm):
	
	class Meta:
		model = tb_reservasWeb
		fields = [
		'mail',
		'nombre',
		'telefono',
		'servicioPrestar'
		
		
		
		]
		exclude = ['dateTurn', 'HoraTurn',"statusTurn", 'montoAPagar', 'description']

		labels = {
		'mail':'ingrese su correo', 
		'nombre': 'ingrese su nombre',
		'telefono':'ingrese su telefono de contacto',
		
		
		}

		widgets = {

		'servicioPrestar': Select(attrs={'id':'servicio','class':'form-control',
			'required':True,
			'autofocus':True,
			'placeholder':'Seleccione el servicio'}),

		
		}



class EditReservaWebForm(forms.ModelForm):
	
	class Meta:
		model = tb_reservasWeb
		fields = [
		'statusTurn',
		
		
		]
		exclude = ['dateTurn', 'servicioPrestar', 'HoraTurn',  'mail', 'client', 'nombre', 'telefono',]

		labels = {
		'statusTurn':'Estatus',
		
		
		}
		widgets = {
		'statusTurn':Select(attrs={'class':'form-control',
			'required':True,
			'autofocus':True,
			'placeholder':'Seleccione el status'}),
		}