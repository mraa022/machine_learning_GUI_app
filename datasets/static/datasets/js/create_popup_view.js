function form_valid(response){

	return  $(response).find('.alert').text().length ==0 

}


function add_errors_to_form(form,response){

	form.prepend($(response).find('.alert'));
}

function get_data(){
	var form_data = new FormData();
	var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
	var url = $("input[type='url']").val();
	var files = $('input[type="file"]')[0].files[0];
	form_data.append('file',files);
	form_data.append('csrfmiddlewaretoken',csrf_token);
	form_data.append('link',url);
	return form_data;
}

function remove_previous_errors(){
	$('.alert').remove();
}

$(function() {
	var modal_body = $('.modal-body');
	var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
	$('#create-dataset').submit(function(e){
			e.preventDefault();
			remove_previous_errors();
			var data = get_data();
			$.ajax({
				type:'POST',
				url: "/datasets/create/",
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