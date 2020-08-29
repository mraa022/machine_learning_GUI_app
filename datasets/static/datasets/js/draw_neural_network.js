var neural_network_graph = document.getElementById('neural_network_graph').getContext('2d');
var neural_network_canvas = document.getElementById('neural_network_graph');

var activation_function_options = "<select style='width:12%;' class='browser-default custom-select custom-select-lg mb-3 optimizer-options'> <option value='relu' class='dropdown-item'>relu</option> <option value = 'sigmoid' class='dropdown-item'>sigmoid</option> <option value = 'softmax' class='dropdown-item'>softmax</option> <option value = 'softplus' class='dropdown-item'>softplus</option> <option value = 'softsign' class='dropdown-item'>softsign</option> <option value = 'tanh' class='dropdown-item'>tanh</option> <option value = 'selu' class='dropdown-item'>selu</option> <option value = 'elu' class='dropdown-item'>elu</option> <option value = 'exponential' class='dropdown-item'>exponential</option> </select >"
var layers_horizontal_gap = 8
var radius = 20;
var right_shift_first_layer_by = radius  
var diameter = radius*2;
function draw_neuron() {

    neural_network_graph.beginPath();
    neural_network_graph.arc(layer_x, layer_vertical_position, radius, starting_angle, end_angle);
    neural_network_graph.stroke();
    neural_network_graph.closePath();

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

function finished_drawing_neuron(end_angle){
	return end_angle > Math.PI*2.3;
}


function draw_connection(){

	neural_network_graph.beginPath();
    neural_network_graph.moveTo(start_x, start_y);
    neural_network_graph.lineTo(end_x, end_y);
    neural_network_graph.stroke();
    neural_network_graph.closePath();

}

function finished_drawing_connection(end_x,next_layer_number,x_accumulator){

	console.log(end_x);
	let start_of_new_layer = get_horizontal_position_of_layer(next_layer_number);
	return Math.floor(end_x) == start_of_new_layer+x_accumulator
	// end_x = (4*diameter)*2;
	
	// end_x_ = ((right_shift_first_layer_by)+(radius*layers_horizontal_gap)-radius)*layer_number;
	// end_y_ = get_vertical_position_of_layer(next_layer_neurons)
	// return (end_x == end_x_ && end_y_==end_y_)
}

function finished_drawing_layer_connections(start_y,layer_neurons){
	// console.log(get_height_of_layer(layer_neurons) , (end_y+radius))
	
	let center_of_bottom_most_neuron = get_vertical_position_of_layer(layer_neurons) // center of y
	let top_most_neuron = (center_of_bottom_most_neuron*layer_neurons) + radius // radius is added to get the top
	return start_y == top_most_neuron  

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

function get_x_accumulator(x_of_current_layer_neuron,x_of_next_layer_neuron){
	return (x_of_next_layer_neuron-x_of_current_layer_neuron)*0.25 // add this value to end_x every time 
}

function get_y_accumulator(y_of_current_layer_neuron,y_of_next_layer_neuron){
	return (y_of_current_layer_neuron-y_of_next_layer_neuron)*0.25 // add this value to end_y every time 
}
function get_y_of_neuron(layer_neurons,neuron_number){
	if (neuron_number == 1){
		return get_vertical_position_of_layer(layer_neurons)
	}
	return get_vertical_position_of_layer(layer_neurons) + (neuron_number*diameter)
}


var neuron_connection_animation_id = null;
var current_layer = 0


var start_x;
var start_y;
var end_x;
var end_y;
var current_layer_neuron_number = 1
var next_layer_neuron_number = 1;
function animate_neuron_connections(){
	let current_layer_neurons = layer_neurons_list[current_layer];
	let next_layer = current_layer+1
	let next_layer_neurons = layer_neurons_list[next_layer];
	let current_layer_vertical_position = get_vertical_position_of_layer(current_layer_neurons)
	let next_layer_vertical_position = get_vertical_position_of_layer(next_layer_neurons)
	let x_of_current_layer_neuron = get_horizontal_position_of_layer(current_layer);
	let y_of_current_layer_neuron = get_y_of_neuron(current_layer_neurons,current_layer_neuron_number);
	let x_of_next_layer_neuron = get_horizontal_position_of_layer(next_layer);
	let y_of_next_layer_neuron = get_y_of_neuron(next_layer_neurons,next_layer_neuron_number);
	let x_accumulator = get_x_accumulator(x_of_current_layer_neuron,x_of_next_layer_neuron);
	let y_accumulator = get_y_accumulator(y_of_current_layer_neuron,y_of_next_layer_neuron)
    draw_connection();

    start_x+=x_accumulator;
    end_x += x_accumulator
    end_y += y_accumulator
    // start_y += y_accumulator
   	
    if(next_layer > layer_neurons_list.length){
    	console.log('no more layers')
    	cancelAnimationFrame(neuron_connection_animation_id);
    	return
    }
   
    if (finished_drawing_connection(end_x,next_layer,x_accumulator) && next_layer <=layer_neurons_list.length) {
    	next_layer_neuron_number+=1;
    	
    	x_of_next_layer_neuron = get_horizontal_position_of_layer(next_layer);
		y_of_next_layer_neuron = get_y_of_neuron(next_layer_neurons,next_layer_neuron_number);
        start_x = get_horizontal_position_of_layer(current_layer);
        start_y = get_y_of_neuron(current_layer_neurons,current_layer_neuron_number);
        end_x = start_x + get_x_accumulator(x_of_current_layer_neuron,x_of_next_layer_neuron)
        end_y = start_y

        // 160 760

        // 40 380 800 380
  //       start_x = diameter
		// start_y = (get_vertical_position_of_layer(layer_neurons_list[0]))
		// end_x = start_x+get_x_accumulator(diameter,get_horizontal_position_of_layer(1));
		// end_y = start_y;
       
        
    }

    neuron_connection_animation_id = requestAnimationFrame(animate_neuron_connections);



}



var layer_number = 0
var neuron_number = 0
var layer_neurons_list
var layer_x = right_shift_first_layer_by
var layer_vertical_position = neural_network_canvas.height - (radius)
var starting_angle = 0
var end_angle = 1
var neuron_drawing_animation_id = null;
function animate_neuron_drawing(layer_neurons) {
    if (layer_ended(neuron_number, layer_neurons_list[layer_number]) && at_least_1_layer_remaining(layer_number, layer_neurons_list.length) ) {
        
            layer_x += (radius * layers_horizontal_gap);
            neuron_number = 0
            layer_number += 1;
            layer_vertical_position = (neural_network_canvas.height - (radius)) - ((Math.max(...layer_neurons_list) - layer_neurons_list[layer_number]) * radius)

        } 
    else if(layer_ended(neuron_number, layer_neurons_list[layer_number]) && !at_least_1_layer_remaining(layer_number, layer_neurons_list.length)) {
        reset_everything();
        // animate_neuron_connections();
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
        layer_vertical_position -= diameter;
    }


    neuron_drawing_animation_id = requestAnimationFrame(animate_neuron_drawing);

}



var first_time_animated = 0;
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
    	console.log(layer_neurons_list);
		

        layer_vertical_position = (neural_network_canvas.height - radius) - ((Math.max(...layer_neurons) - layer_neurons[0]) * radius); // center the first layer
        
        
        if (first_time_animated!=0) {
        	reset_everything();
        	layer_vertical_position = (neural_network_canvas.height - (radius)) - ((Math.max(...layer_neurons) - layer_neurons[0]) * radius); // center the first layer.(clears its previous value)
        	cancelAnimationFrame(neuron_drawing_animation_id)
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