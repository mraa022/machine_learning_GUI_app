function get_chosen_optimizer(){
    return  $('.optimizer-options').val();

}

function get_loss(){
    return $('.loss-options').val()
}

function update_graph(data){

    
    if(data.clear_graph){
        console.log('CLEAR THE GRAPH')
        lineChart.data.datasets[0].data = []; // clear training loss
        lineChart.data.datasets[1].data = []; // clear test loss
        lineChart.data.labels = []; // clear x-axis
        lineChart.update()
    }

    
    if (data.numbers_got_too_big=='No') {
        let dataset = lineChart.data.datasets[0]
        lineChart.data.labels.push(dataset.data.length + 1);
        lineChart.data.datasets[0].data.push(data.training_loss); 
        lineChart.data.datasets[1].data.push(data.test_loss);
        lineChart.update();

    }
    else if (data.numbers_got_too_big == 'Yes'){
        alert('the loss got too big, so the model stoped training.')
    }



}
function get_layers(){
	let layer_neurons = []
	let layers_list = $('.layers input');
    for (let i = 0; i < layers_list.length; i++) {

        if (layers_list[i].value.length > 0 && layers_list[i].value > 0) { // if layer is > 0 
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

        if (layers_list[i].value.length > 0 && layers_list[i].value > 0) { // if layer > 0
            layer_activations.push(layer_activations_list[i].value) // get that layer's activation func
        }

    }
    return layer_activations

}

function get_optimizer_params(){

    let optimizer_params = $('.optimizer-params input').filter(function(){
        return $(this).css('display')!='none'
    }); // get the visible parameters. 'handle_losses_and_optimizer_options.js' takes care of making some parameters visible based on the optimizer

    let optimizer_params_and_values = {}
    optimizer_params.each(function (){
        let param_name = $(this).attr('id'); 
        let param_value = parseFloat($(this).val())
        
        optimizer_params_and_values[param_name] = param_value;
        
        
    })

    return optimizer_params_and_values


}


var error_rate_canvas = document.getElementById('error_rate');

var datasets = {
		    labels: [],
		    datasets: [{
		        label: "Training Loss",
		        data: [],
		        fill: false,
		        borderColor: "#bae755",
                pointRadius: 0.5
		    },
            {
                label:'Test Loss',
                data:[],
                fill:false,
                borderColor: 'red',
                pointRadius: 0.5

            }
            
            ]
		}
var lineChart = new Chart(error_rate_canvas, {
		    type: 'line',
		    data: datasets
		});

var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var websocket_is_open = false
var errorRateSocket = new WebSocket(
        ws_scheme 
        +
        '://' 
        +
        window.location.host
       	+
        '/ws/error_graph/' 
     	
    )

errorRateSocket.onopen = function (event){
    websocket_is_open = true;
}

errorRateSocket.onmessage = function(e) {

        const data = JSON.parse(e.data);
        if(data.invalid_input){
            alert(data.invalid_input);
        }

        if(data.can_train_new_model){ // send a message from consumer at the beginning of training  so another model can be trainined (train model button is unabled)
            $('#train_neural_network').prop('disabled', false)
        }
        else{
            update_graph(data);
        }
    }

let first_time = true
$('#train_neural_network').on('click',function(e){
    
    
    $("*").animate({ scrollTop: $(document).height() }, 1000); // scroll to the bottom of the page where the error graph is
    $('#train_neural_network').prop('disabled', true);
    
    

    if (websocket_is_open){
        errorRateSocket.send(JSON.stringify({
            'layers': get_layers(),
            'layer_activations':get_layer_activations(),
            'optimizer_params':get_optimizer_params(),
            'label_type':Cookies.get('label_is'),
            'label_column':Cookies.get('label_column'),
            'optimizer':get_chosen_optimizer(),
            'loss':get_loss(),
            'batch_size':$('#batch-size').val(),
            'test_size':$('#test-percent').val(),
            }));

    }
   
        first_time = false;
    
});