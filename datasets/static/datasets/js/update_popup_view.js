$(function() {
	var modal_body = $('.modal-body');
	var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
	$('#update-dataset').submit(function(e){
			var pk = $('#pk').text();
			var clear_file_field = $('#file-clear_id').is(':checked');
			e.preventDefault();
			$('.alert').remove();
			var url = $("input[type='url']").val();
			var fd = new FormData();
			var files = $('input[type="file"]')[0].files[0];
			fd.append('file',files);
			fd.append('csrfmiddlewaretoken',csrf_token);
			fd.append('link',url);
			fd.append('clear-previous-file',clear_file_field);
			$.ajax({
				type:'POST',
				url: "/datasets/update/"+pk+"/",
				data: fd,
				contentType: false,
				processData:false,
				success: function(response){
						modal_body.prepend($(response).find('.alert'));
					if ($(response).find('.alert').text().length ==0) {
						console.log($('#modal-update'));
						$("#modal-update").removeClass("in");
    					$(".modal-backdrop").remove();
  						$("#modal-update").hide();
  						location.reload();
					}
				},
				
			});
			
	
	});
	});