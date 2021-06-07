var server_address = "http://34.89.189.185:5000/"; //ID Estatica Microservicios

var info_device = function (){
    var id_device= id_select();
    var json = {"id_device":id_device};

    $.post( server_address + "nombre_device/", { id_device: id_select() }, function( data ) {

        var aux ="";
        for (var i=0;i<data.id.length;i++){
            id = "ID: ";
            mac = " Dispositivo : ";
            GPS = " Ubicación: ";
            aux += "<tr>";
            aux += "<td>" +"<a class='tipo_sensor'>" + id + "<a>"+ data.id[i] + "</a>";
            aux += "<td>" +"<a class='tipo_sensor'>" + mac+ "<a>"+ data.device[i] + "</td>";
            aux += "<td>" +"<a class='tipo_sensor'>" + GPS + "<a>"+ data.GPS[i] + "</td>";
            aux += "</tr>";
        }
        $(".nombreSensor").html(aux);
    });
}

function get_measures(){
    $.post( server_address + "sensor_list/", { id_device: id_select() }, function( data ) {
        var aux ="<table><tr><th class='td'>Fecha</th><th class='td'>Temperatura</th><th class='td'>Humedad</th></tr>";
        for (var i=0;i<data.id.length;i++){
            aux += "<tr>";
            aux += "<td class='td'>" + data.fecha[i] + "</td>";
            aux += "<td class='td'>" + data.temperature[i] + "</td>";
            aux += "<td class='td'>" + data.humidity[i] + "</td>";
        }
        aux += "<table>";
        $(".data").html(aux);
    }, "json");
}

function id_select() {
var sPaginaURL = window.location.search.substring(1);
 var sURLVariables = sPaginaURL.split('&');
  for (var i = 0; i < sURLVariables.length; i++) {
    var sParametro = sURLVariables[i].split('=');
    if (sParametro[0] == "device_id") {
      return sParametro[1];
    }
  }
 return null;
}

function volver(){
    window.location= "Front_Dispositivos.html";
}

function get_measures_filtered(){
    var inicio = document.getElementById("fecha_inicial").value;
    var fin = document.getElementById("fecha_final").value;

    if (inicio <= fin & inicio!="" & fin!="") {
        $.post(server_address + "sensor_list_filtrado/", {
            id_device: id_select(),
            fecha_inicio: inicio,
            fecha_fin: fin
        }, function (data) {
            var aux = "<table><tr><th class='td'>Fecha</th><th class='td'>Temperatura</th><th class='td'>Humedad</th></tr>";
            for (var i = 0; i < data.id.length; i++) {
                aux += "<tr>";
                aux += "<td class='td'>" + data.fecha[i] + "</td>";
                aux += "<td class='td'>" + data.temperature[i] + "</td>";
                aux += "<td class='td'>" + data.humidity[i] + "</td>";
            }
            aux += "<table>";
            $(".data").html(aux);
        }, "json");
      }else{
        alert("El orden de las fechas es incorrecto, o existe un campo vacío")
    }

}

var music = new Audio('refresh.mp3');
var actualizar= function (){
        music.play();
        get_measures();
}

info_device();
get_measures();