$(function() {
	var modal_body = $('.modal-body');
	var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
	$('#create-dataset').submit(function(e){
			e.preventDefault();
			$('.alert').remove();
			var url = $("input[type='url']").val();
			var fd = new FormData();
			var files = $('#id_file')[0].files[0]
			fd.append('file',files);
			fd.append('csrfmiddlewaretoken',csrf_token);
			fd.append('link',url);
			$.ajax({
				type:'POST',
				url: "/datasets/create/",
				data: fd,
				contentType: false,
				processData:false,
				success: function(response){
						modal_body.prepend($(response).find('.alert'));
					if ($(response).find('.alert').text().length ==0) {

						
						location.reload();
						

					}
				},
			
			});
			
	
	});
	});