function form_valid(response){

	return  $(response).find('.alert').text().length ==0 

}

function add_errors_to_form(form,response){

	form.prepend($(response).find('.alert'));
}

function clear_cookies(){
	Cookies.set('primary_key','',{path:'/'});
	Cookies.set('dataset_location', '', {path: '/' });
}

function remove_previous_errors(){
	$('.alert').remove();
}

$(function() {
	var modal_body = $('.modal-body');
	var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
	$('#choose-new-dataset').submit(function(e){
			e.preventDefault();
			$('#can_continue').css('display','none');	// remove the 'continue' button
			remove_previous_errors(); 
			clear_cookies() // clear the cookies that store the pk and url/file path of the selected dataset. (this new dataset's location is saved in the session)
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
					if (form_valid(response)){
							window.location = '/datasets/regression_or_classification/'
						}
						else{
							add_errors_to_form(modal_body,response); 
						}
				},
			
			});
			
	
	});
	});