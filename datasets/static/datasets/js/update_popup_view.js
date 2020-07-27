function get_data(){

	var form_data = new FormData();
	var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
	var clear_file_field = $('#file-clear_id').is(':checked'); 
	var url = $("input[type='url']").val();
	var files = $('input[type="file"]')[0].files[0];
	form_data.append('file',files);
	form_data.append('csrfmiddlewaretoken',csrf_token);
	form_data.append('link',url);
	form_data.append('clear-previous-file',clear_file_field);
	return form_data;
}

function remove_previous_errors(){
	$('.alert').remove();
}

function form_valid(response){

	return  $(response).find('.alert').text().length ==0 

}

function add_errors_to_form(form,response){

	form.prepend($(response).find('.alert'));
}

$(function() {
	var modal_body = $('.modal-body');
	$('#update-dataset').submit(function(e){
			var pk = $('#pk').text();
			var data = get_data();
			e.preventDefault();
			remove_previous_errors();
			$.ajax({
				type:'POST',
				url: "/datasets/update/"+pk+"/",
				data: data,
				contentType: false,
				processData:false,
				success: function(response){
						if (form_valid(response)){
							location.reload();
						}
						else{
							add_errors_to_form(modal_body,response);
						}
				},
				
			});
			
	
	});
	});