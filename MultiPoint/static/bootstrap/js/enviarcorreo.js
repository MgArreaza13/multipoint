function EnviarCorreo() {
	$('#BotonEnviar').attr('disabled', 'disabled');
	var asunto = $('#Asunto').val();
	var mail   = $('#compose-textarea').val();
	var screen = $('#loading-screen');

    configureLoadingScreen(screen);
    $.ajax({
		    // la URL para la petición
		    url : '/marketing/Nuevo/Envio/de/correo/masivo',
		    // la información a enviar
		    // (también es posible utilizar una cadena de datos)
		    data : { 
		    	'asunto':asunto,
		    	'mail':mail,
		    },
		    // el tipo de información que se espera de respuesta
		    dataType : 'json',
		    // código a ejecutar si la petición es satisfactoria;
		    // la respuesta es pasada como argumento a la función
		    success : function(status) {
		    	if (status == 200) {
		    		//todo correcto 
		    		swal("Felicidades!", "Hemos Enviado Completamente su correo a todos los email registrados!", "success")
		        	location.href ="/marketing/";
		    	}
		    	else{
		    		$('#BotonEnviar').removeAttr('disabled');
		    		swal("OOOh!", "Ha pasado un problema intente nuevamente por favor", "error")
		    	}
		    },
		 
		    // código a ejecutar si la petición falla;
		    // son pasados como argumentos a la función
		    // el objeto de la petición en crudo y código de estatus de la petición
		    error : function(xhr, status) {
		    	$('#BotonEnviar').removeAttr('disabled');
		        swal("OOOh!", "Hemos tenido un problema con el Servidor!", "error")
		    },
		 
		    // código a ejecutar sin importar si la petición falló o n
		});
}

function configureLoadingScreen(screen){
    $(document)
        .ajaxStart(function () {
            screen.fadeIn();
        })
        .ajaxStop(function () {
            screen.fadeOut();
        });
}


