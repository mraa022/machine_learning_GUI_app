
function show_loading_screen(){

	$('#dataframe .modal-content').html('<div style="background-color:black;" align="center"><i class="fas fa-spinner fa-10x fa-spin"></i></div>')

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