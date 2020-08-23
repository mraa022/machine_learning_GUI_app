function update_graph(data){

	lineChart.data.datasets.forEach((dataset) => {
            lineChart.data.labels.push(dataset.data.length + 1);
            dataset.data.push(data.error_rate);
            
        	});
    lineChart.update();

}

function get_layers(){
	let layer_neurons = []
	let layers_list = $('.layers input');
    for (let i = 0; i < layers_list.length; i++) {

        if (layers_list[i].value.length > 0 && layers_list[i].value > 0) { // if layer is not empty
            layer_neurons.push(layers_list[i].value)
        }

    }
    return layer_neurons
}

function get_layer_activations(){

	let layer_activations = []
	let layers_list = $('.layers input');
	let layer_activations_list = $('.activation_function_options select')
    for (let i = 0; i < layers_list.length; i++) {

        if (layers_list[i].value.length > 0 && layers_list[i].value > 0) { // if layer is not empty
            layer_activations.push(layer_activations_list[i].value)
        }

    }
    return layer_activations

}
var error_rate_canvas = document.getElementById('error_rate');
var datasets = {
		    labels: [],
		    datasets: [{
		        label: "Training Loss",
		        data: [],
		        fill: false,
		        borderColor: "#bae755"
		    }]
		}
var lineChart = new Chart(error_rate_canvas, {
		    type: 'line',
		    data: datasets
		});

var number_of_times_connected = 0
var errorRateSocket = new WebSocket(
        'ws://' +
        window.location.host
       	+
        '/ws/error_graph/' 
     	
    )

errorRateSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        update_graph(data);
        

	}
$('#train_neural_network').on('click',function(e){


    errorRateSocket.send(JSON.stringify({
        'layers': get_layers(),
        'layer_activations':get_layer_activations()
    }));

    
});