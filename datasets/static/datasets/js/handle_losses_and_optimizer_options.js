
function show_optimizer_params(){

	let all_optimzer_params = $('.optimizer-params');
	let chosen_optimizer = $('.optimizer-options').val();
	let every_optimzer_params = {
		Adam:['learning_rate','beta_1','beta_2'],
		Rmsprop:['learning_rate','rho','momentum'],
		Adagrad:['learning_rate','initial_accumulator_value'],
		Adadelta:['learning_rate','rho'],
		SGD:['learning_rate','momentum'],
		Adamx:['learning_rate','beta_1','beta_2'],
		Nadam:['learning_rate','beta_1','beta_2'],
		Ftrl:['learning_rate','learning_rate_power','initial_accumulator_value','l1_regularization_strength','l2_regularization_strength','l2_shrinkage_regularization_strength']

	}
	let params_to_show = every_optimzer_params[chosen_optimizer];

	
	$('.optimizer-params').children().fadeOut(500);
	for(let i = 0;i<params_to_show.length;i++){
		
		$('#'+params_to_show[i]).fadeIn(500);
	}


}
show_optimizer_params();
$('.optimizer-options').change(function (){
	show_optimizer_params();
});
if(Cookies.get('label_is') == 'discrete'){
	let discrete_loss_options = ['CategoricalCrossentropy','Poisson','KLDivergence','BinaryCrossentropy']
	for(let option = 0; option< discrete_loss_options.length;option++){
		
		$('.loss-options').append($('<option></option>').attr('value',discrete_loss_options[option]).text(discrete_loss_options[option]));
		
	}

}

else{

	let continuous_loss_options = ['MeanSquaredError','MeanAbsoluteError','MeanAbsolutePercentageError','MeanSquaredLogarithmicError','CosineSimilarity','Huber','LogCosh']
	for(let option = 0; option< continuous_loss_options.length;option++){
		$('.loss-options').append($('<option></option>').attr('value',continuous_loss_options[option]).text(continuous_loss_options[option]));
	}

}

