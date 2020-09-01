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

function replace_top_half_with_head_of_dataframe(){

	$.get('/datasets/selected_dataset/',function(response){ 
			$('.not-modal-jumbotron').html(response);
			});

}
function replace_bottom_half_of_page(){

	$.get("/datasets/regression_or_classification/",function(response){ 
		$("#modal .close").click()
		$('.ajax_part_of_page').html(response); 

		});

}

function show_loading_screen(){
	$('.not-modal-jumbotron').html('<img src="https://theplaycave.com.au/wp-content/uploads/2016/10/loading.gif">'); // show laoding gif

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
							clear_cookies(); // if a new dataset is chosen, its location, is saved in the session,not cookies.
							show_loading_screen() // show laoding gif in the top half of the page
							replace_top_half_with_head_of_dataframe();// replace the top half of the page with the first 5 rows of the chosen dataset
							replace_bottom_half_of_page() // replace the bottom half of the page with the classification_or_regression page.
						}
						else{
							add_errors_to_form(modal_body,response); 
						}
				},
			
			});
			
	
	});
	});