var c = document.getElementById("neural_network_canvas");
var ctx = c.getContext("2d");


var radius = 20;
var sangle = 50;
var eangle = 0;

for (var i = 0; i <10;i++){

	ctx.beginPath();
	ctx.arc(100,i*(radius*2.5),radius,sangle,eangle,2*Math.PI);
	ctx.stroke();
	ctx.closePath();
}