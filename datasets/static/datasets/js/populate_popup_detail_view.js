$('.view').on('click',function(){
			id_ = $(this).attr('id') // the id of the submit button is the primary key	
			$('#dataframe .modal-content').html('<img src="https://theplaycave.com.au/wp-content/uploads/2016/10/loading.gif">')
			$.ajax({
				type:'GET',
				dataType:'html',
				url: '/datasets/dataset/'+id_+'/',
				success: function(e){
					$('#dataframe .modal-content').html($(e).find('.jumbotron'));  
				}

			});

	});