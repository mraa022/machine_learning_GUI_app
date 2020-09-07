var neural_network_context = document.getElementById('neural_network_graph').getContext('2d');
var neural_network_canvas = document.getElementById('neural_network_graph');

var activation_function_options = "<select style='width:12%;' class='browser-default custom-select custom-select-lg mb-3 optimizer-options'> <option value='relu' class='dropdown-item'>relu</option> <option value = 'sigmoid' class='dropdown-item'>sigmoid</option> <option value = 'softmax' class='dropdown-item'>softmax</option> <option value = 'softplus' class='dropdown-item'>softplus</option> <option value = 'softsign' class='dropdown-item'>softsign</option> <option value = 'tanh' class='dropdown-item'>tanh</option> <option value = 'selu' class='dropdown-item'>selu</option> <option value = 'elu' class='dropdown-item'>elu</option> <option value = 'exponential' class='dropdown-item'>exponential</option> </select >"
var layers_horizontal_gap = (radius*8)
var radius = 20;
var right_shift_first_layer_by = radius  
var diameter = radius*2;
function draw_neuron() {

    neural_network_context.beginPath();
    neural_network_context.arc(layer_x, layer_vertical_position, radius, starting_angle, end_angle);
    neural_network_context.stroke();
    neural_network_context.closePath();

}


function layer_ended(neuron_number,layer_neurons_number){
	return neuron_number == layer_neurons_number;
}

function at_least_1_layer_remaining(layer_number,number_of_layers){
	return layer_number+1 != number_of_layers
}


function reset_everything(){

	layer_number = 0;
    neuron_number = 0;
    starting_angle = 0;
    end_angle = 1;
    layer_x = radius;

}


function get_vertical_position_of_layer(layer_neurons){
	return (neural_network_canvas.height - (radius)) - ((Math.max(...layer_neurons_list) - layer_neurons) * radius);
}

function get_horizontal_position_of_layer(layer_number){

	if (layer_number == 0){
		return diameter;
	}
	return (4*radius)*(layer_number+1) // one is added because layer_number starts from 0


}

var layer_number = 0
var neuron_number = 0
var layer_neurons_list
var layer_x = right_shift_first_layer_by
var layer_vertical_position
var starting_angle = 0
var end_angle = 1
var neuron_drawing_animation_id = null;
function animate_neuron_drawing(layer_neurons) {
    if (layer_ended(neuron_number, layer_neurons_list[layer_number]) && at_least_1_layer_remaining(layer_number, layer_neurons_list.length) ) {
        
            layer_x +=  layers_horizontal_gap;
            neuron_number = 0
            layer_number += 1;
            layer_vertical_position = get_vertical_position_of_layer(layer_neurons_list[layer_number])  // get vertical position of next layer

        } 
    else if(layer_ended(neuron_number, layer_neurons_list[layer_number]) && !at_least_1_layer_remaining(layer_number, layer_neurons_list.length)) {
        reset_everything();
        cancelAnimationFrame(neuron_drawing_animation_id);
        return;
    }

    draw_neuron();

    starting_angle += 1
    end_angle += 1
    if (finished_drawing_neuron(end_angle)) {

        starting_angle = 0;
        end_angle = 1;
        neuron_number += 1;
        layer_vertical_position -= diameter; // move to drawing the neuron above.
    }


    neuron_drawing_animation_id = requestAnimationFrame(animate_neuron_drawing);

}



var first_time_animated = true;
$('#build-neural-network').on('click', function(e) {

    var layers_list = $('.layers input');
    var layer_neurons = []
    for (let i = 0; i < layers_list.length; i++) {

        if (layers_list[i].value.length > 0 && layers_list[i].value > 0) {
            layer_neurons.push(layers_list[i].value)
        }   
    }

    if (layer_neurons.length != 0) {

        neural_network_canvas.height = Math.max(...layer_neurons) * diameter;
        neural_network_canvas.width = (layer_neurons.length) * (diameter * 4);
        layer_neurons_list = layer_neurons;
		

        layer_vertical_position = (neural_network_canvas.height - radius) - ((Math.max(...layer_neurons) - layer_neurons[0]) * radius); // center the first layer
        
        
        if (!first_time_animated) {
        	reset_everything();
        	layer_vertical_position = (neural_network_canvas.height - (radius)) - ((Math.max(...layer_neurons) - layer_neurons[0]) * radius); // center the first layer.(clears its previous value)
        	cancelAnimationFrame(neuron_drawing_animation_id)
        }
       
   
		
        animate_neuron_drawing(layer_neurons);
        first_time_animated = false;

    }

});


//////// adding layers and their activation funcs
$('#add-layer').click(function() {
    let layers_div = $('.layers');
    let activation_function_options_div = $('.activation_function_options');
    activation_function_options_div.append(activation_function_options);
    layers_div.append('<input style="width:12%" type="number" placeholder="Number of Neurons"></input>');
});