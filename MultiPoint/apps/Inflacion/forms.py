from django import forms
from django.forms import ModelForm, Textarea, Select
from apps.Inflacion.models import tb_inflacion

class InflacionForm(forms.ModelForm):
	
	class Meta:
		model = tb_inflacion
		fields = [
		'Enero',
		'Febrero',
		'Marzo',
		'Abril',
		'Mayo',
		'Junio',
		'Julio',
		'Agosto',
		'Septiembre',
		'Octubre',
		'Noviembre',
		'Diciembre',
		

		
		]
		exclude = ['user', 'dateCreate',]

		labels = {
		
		'Enero':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Enero',
		'Febrero':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Febrero',
		'Marzo':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Marzo',
		'Abril':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Abril',
		'Mayo':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Mayo',
		'Junio':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Junio',
		'Julio':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Julio',
		'Agosto':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Agosto',
		'Septiembre':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Septiembre',
		'Octubre':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Octubre',
		'Noviembre':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Noviembre',
		'Diciembre':'Ingrese el porcentaje de inflacion para multiplicar los productos y servicios de Diciembre',
		
		}