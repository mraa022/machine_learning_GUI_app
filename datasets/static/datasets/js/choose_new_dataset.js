$(function() {
	var modal_body = $('.modal-body');
	var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
	$('#choose-new-dataset').submit(function(e){

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
				url: "/datasets/choose_new_dataset/",
				data: fd,
				contentType: false,
				processData:false,
				success: function(response){
						modal_body.prepend($(response).find('.alert'));
					if ($(response).find('.alert').text().length ==0) {
					

						// clear the cookies, new datasets are stored in a session
						Cookies.set('primary_key','',{path:'/'});
						Cookies.set('dataset_location', '', {path: '/' });
						location.reload();
						
					}
				},
			
			});
			
	
	});
	});