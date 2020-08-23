var neural_network_graph = document.getElementById('neural_network_graph').getContext('2d');
var neural_network_canvas = document.getElementById('neural_network_graph');
let radius = 20;
var layer_x = radius + 5
var layer_vertical_position = neural_network_canvas.height - (radius)

var starting_angle = 0
var end_angle = 1
var activation_function_options = "<select style='width:12%;' class='browser-default custom-select custom-select-lg mb-3 optimizer-options'> <option value='relu' class='dropdown-item'>relu</option> <option value = 'sigmoid' class='dropdown-item'>sigmoid</option> <option value = 'softmax' class='dropdown-item'>softmax</option> <option value = 'softplus' class='dropdown-item'>softplus</option> <option value = 'softsign' class='dropdown-item'>softsign</option> <option value = 'tanh' class='dropdown-item'>tanh</option> <option value = 'selu' class='dropdown-item'>selu</option> <option value = 'elu' class='dropdown-item'>elu</option> <option value = 'exponential' class='dropdown-item'>exponential</option> </select >"
function draw() {

    neural_network_graph.beginPath();
    neural_network_graph.arc(layer_x, layer_vertical_position, radius, starting_angle, end_angle);
    neural_network_graph.stroke();
    neural_network_graph.closePath();

}

var layer_number = 0
var neuron_number = 0
var layer_neurons_list

function first_time_called(layer_neurons){
	return typeof(layer_neurons) == 'object';
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
    layer_x = radius + 5;

}
var id = null;
function finished_drawing_neuron(end_angle){
	return end_angle > Math.PI*2.1;
}
function animate_neuron_drawing(layer_neurons) {
    if (first_time_called(layer_neurons)) {  // the 'layer_neurons' parameter changes after the first call of this func since its being called forever and not provided the 'layer_neurons' argument after the first time
        layer_neurons_list = layer_neurons;
    }

    if (layer_ended(neuron_number, layer_neurons_list[layer_number]) && at_least_1_layer_remaining(layer_number, layer_neurons_list.length) ) {
        
            layer_x += (radius * 4);
            neuron_number = 0
            layer_number += 1;
            layer_vertical_position = (neural_network_canvas.height - (radius)) - ((Math.max(...layer_neurons_list) - layer_neurons_list[layer_number]) * radius)

        } 
    else if(layer_ended(neuron_number, layer_neurons_list[layer_number]) && !at_least_1_layer_remaining(layer_number, layer_neurons_list.length)) {
        reset_everything();
        return;
        // cancelAnimationFrame(id);

    }

    
    draw();

    starting_angle += 1
    end_angle += 1
    if (finished_drawing_neuron(end_angle)) {
        starting_angle = 0;
        end_angle = 1;
        neuron_number += 1;
        layer_vertical_position -= (radius * 2);
    }

    id = requestAnimationFrame(animate_neuron_drawing);
}

var first_time_animated = 0;
$('#build-neural-network').on('click', function() {

	
    var layers_list = $('.layers input');
    var layer_neurons = []
    for (let i = 0; i < layers_list.length; i++) {

        if (layers_list[i].value.length > 0 && layers_list[i].value > 0) {
            layer_neurons.push(layers_list[i].value)
        }
    }
    if (layer_neurons.length != 0) {
        neural_network_canvas.height = Math.max(...layer_neurons) * (radius * 2);
        neural_network_canvas.width = (layer_neurons.length) * ((radius * 2) * 3);

        layer_vertical_position = (neural_network_canvas.height - (radius)) - ((Math.max(...layer_neurons) - layer_neurons[0]) * radius); // center the first layer
        if (first_time_animated!=0) {
        	reset_everything();
        	layer_vertical_position = (neural_network_canvas.height - (radius)) - ((Math.max(...layer_neurons) - layer_neurons[0]) * radius); // center the first layer
        	cancelAnimationFrame(id)
        }
        animate_neuron_drawing(layer_neurons);
        first_time_animated++;

    }

});
$('#add-layer').click(function() {
    let layers_div = $('.layers');
    let activation_function_options_div = $('.activation_function_options');
    activation_function_options_div.append(activation_function_options);
    layers_div.append('<input style="width:12%" type="number" placeholder="Number of Neurons"></input>');
});