var server_address = "http://34.89.189.185:5000/"; //ID Estatica Microservicios

var get_devices = function () {
    $.get(server_address + "device_list/" , function (data){
        var aux ="<table><tr><th>ID</th><th>Devices</th><th>Estado</th><th>Ubicacion</th><th>Fecha</th><th>Ver Resultados</th><th>Desactivar</th></tr>";
        for (var i=0;i<data.id.length;i++){
            aux += "<tr>";
            aux += "<td>" + data.id[i] + "</td>";
            aux += "<td>" + data.device[i] + "</td>";
            aux += "<td>" + data.estado[i] + "</td>";
            aux += "<td>" + data.GPS[i] + "</td>";
            aux += "<td>" + data.fecha[i] + "</td>";
            aux += "<td>" + "<button class='boton'  name= '" + data.estado[i] + "' onclick= 'go_sensor(" +data.id[i]+")'>" +"Mostrar" + "</button>"+ "</td>";
            if (data.estado[i] == 'activo') {
                aux += "<td>" + "<button class='boton'  name= '" + data.estado[i] + "' onclick= 'desactivar(" + data.id[i] + ")'>" + "Desactivar" + "</button>" + "</td>";
            }
        }
        aux += "<table>";
        $(".devices").html(aux);
    });
}

var go_sensor = function(id){
    var htmlSensor = "Front_Datos.html";
    window.location= htmlSensor + "?device_id="+id;

}

var desactivar = function(id){
    $.post( server_address + "desactivar/", { id: id }, function(data) {
        get_devices();
    });

}

var music = new Audio('refresh.mp3');
var actualizar= function (){
        music.play();
        get_devices();
}

get_devices();
