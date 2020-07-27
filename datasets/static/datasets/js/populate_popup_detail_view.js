
function show_loading_screen(){

	$('#dataframe .modal-content').html('<img src="https://theplaycave.com.au/wp-content/uploads/2016/10/loading.gif">')

}

function dump_table_in_popup(response){

	$('#dataframe .modal-content').html($(response).find('.jumbotron'));  
}

$('.view').on('click',function(){
			pk = $(this).attr('id') // the id of the submit button is the primary key	
			
			show_loading_screen();
			$.ajax({
				type:'GET',
				dataType:'html',
				url: '/datasets/dataset/'+pk+'/',
				success: function(response){
					dump_table_in_popup(response);
				}

			});

	});