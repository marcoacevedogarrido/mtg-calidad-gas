$(document).ready(function() {

    $('#get_sec_code').click(function () {
        var gas_form_id = window.location.pathname.split('/')[2];
        var url = window.location.origin + "/formulario/"+gas_form_id+"/getform";
        var fetch_sec_code = $.getJSON( url );
        var modal_sec = $('.modal-sec');
        fetch_sec_code.done(function(data){
            modal_sec.append(data.Trama_SEC);
        })
        $('#modalSec').on('hidden.bs.modal', function () { location.reload(); })

    });

    var table_container = $('#dataTable');
    if (table_container.length > 0) {
        var table = table_container.DataTable({
            data: dataTable,
            columns: [
                { title: "ID" },
                { title: "Laboratorista" },
                { title: "Punto Control" },
                { title: "Fecha registro" }
            ]
        });

        $("#dataTable tbody").on('click', 'tr', function () {
            var data = table.row(this).data();
            window.location.href = "/formulario/"+data[0];
        }).on('mouseover', 'tr', function () {
            $('html,body').css('cursor','pointer');
        }).on('mouseout','tr',function () {
            $('html,body').css('cursor','auto');
        });
    }

    var table_container=$("#secTable");
    if (table_container.length>0) {
        var table=table_container.DataTable({
            data:secTable,
            columns:[
                { title: "ID" },
                { title: "Laboratorista" },
                { title: "Punto Control" },
                { title: "Fecha registro" }
            ]
        });
        $("#secTable tbody").on("click","tr", function() {
            var data=table.row(this).data();
            window.location.href ="/formulario/"+data[0];
        }).on("mouseover","tr",function() {
            $("html,body").css("cursor","pointer");
        }).on("mouseout","tr",function() {
            $("html,body").css("cursor","auto");
        });
    }


    var biometano_fields = $('.hidden-field');
    $('#tipo-combustible').change(function () {
        if ($(this).val()==='4') {
            $.each(biometano_fields, function(k,v){
                $(v).removeClass('hidden-field')
            })
        } else {
            $.each(biometano_fields, function(k,v){
                $(v).addClass('hidden-field')
            })
        }
    });

    $('#punto-control').change(function() {
        var name = $(this).val();
        $.get("/api/punto_control/" + name)
            .done(function(data){
                $('#tipo-red').val(data[0]);
                $('#region').val(data[1]);
                $('#tramo').val(data[2]);
            });
    });


    if (window.location.pathname === "/formulario" || window.location.pathname.slice(0,25) === "/mantenedores/eformulario") {
        var url = window.location.origin + '/api/validadores';
        var fetch = $.get(url);
        var validadores = {};
        fetch.done(function(data){
            validadores = data;
        });
    }


    $('#main-form').submit(function (event) {
        event.preventDefault();
        if ($('#fecha_muestra').val() === "") {
            alert('Favor seleccione fecha');
            return
        }

        // Revisamos primero si el gas corresponde a biometano:
        var gas = $('#tipo-combustible').val() === "4" ? 'biometano' : 'normal';
        var form_data = $(this).serializeArray();


        var checking = Object.keys(validadores[gas]['validador_superior']);
        var warnings = [];
        checking.forEach(function (e) {
            var check = validadores[gas]['validador_superior'][e];
            var val = $('#' + e).val();
            if (val > check) {
                warnings.push($($('label[for=' + e + ']')[1]).text() + ", valor max: " + check + ". Ingresado: " + val);
            }
        });
        checking = Object.keys(validadores[gas]['validador_inferior']);
        checking.forEach(function (e) {
            var check = validadores[gas]['validador_inferior'][e];
            var val = $('#' + e).val();
            if (val < check) {
                warnings.push($($('label[for=' + e + ']')[1]).text() + ", valor min: " + check + ". Ingresado: " + val);
            }
        });
        if (warnings) {
            var modal_list = $('.modal-list');
            modal_list.empty();
            warnings.forEach(function (e) {
                modal_list.append('<li>' + e + '</li>')
            });
            $('#myModal').modal()
        } else {
            var posting = $.post(location.href, form_data);
            posting.done(function (data) {
                location.pathname = "/";
            })
        }
        $('#force-save').click(function () {
            var form_data = $('#main-form').serializeArray();
            var posting = $.post(location.href, form_data);
            posting.done(function (data) {
                location.pathname = "/";
            })
        });
    });
});





