var server_address = "http://34.89.189.185:5000/";


var get_last = function() {
    $.get(server_address +  "sensor_data/", function(data){
        $(".result").html("Temperature: "+data.temperature+"ºC | Humidity: "+data.humidity+"%");
    });
}

var get_measures = function () {
    $.get(server_address + "sensor_list/", function(data){
        var aux = "<table><tr><th>ID</th><th>Temperatura</th><th>Humedad</th></tr>";
        for(var i=0; i<data.id.length; i++){
            aux += "<tr>";
            aux += "<td>" +  data.id[i] + "</td>";
            aux += "<td>" +  data.temperature[i] + "</td>";
            aux += "<td>" +  data.humidity[i] + "</td>";
            aux += "<tr>";
        }
        aux += "</table>";
        $(".result").html(aux)
    });
}

var get_devices = function () {
    $.get(server_address + "device_list/", function(data){
        var aux = "<table><tr><th>ID</th><th>Dispositivos</th></tr>";
        for(var i=0; i<data.id.length; i++){
            aux += "<tr>";
            aux += "<td>" +  data.id[i] + "</td>";
            aux += "<td>" +  data.device[i] + "</td>";
            aux += "<tr>";
        }
        aux += "</table>";
        $(".devices").html(aux)
    });
}

var music = new Audio('refresh.mp3');
var actualizar= function (){
        music.play();
        get_devices();
        get_measures();
}
// $.get(server_address,function(data)){
//     $(".principal").html(data.msg);
// }

get_devices();
get_measures();

//setInterval(get_last, 3000);