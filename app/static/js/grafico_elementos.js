var elementos_Chart;
var dataset = {
    time: [],
    agua: [],
    metano: [],
    etano: [],
    propano: [],
    butano: [],
    pentano: [],
    hexano: [],
    nitrogeno: [],
    propano_e_hidrocarburos_superiores: [],
    hexano_hydrocarburos: [],
    hidrogeno: [],
    monoxido_carobono: [],
    porcentaje_vol_gas: [],
    poder_calorifico_superior: [],
    poder_calorifico_inferior: [],
    indice_wobbe: [],
    densidad_relativa: [],
    gases_inertes_pmol: [],
    punto_rocio_hydrocarburos: [],
    resultado_odorizacion: [],
    resultado_impurezas: []
};

function create_chart() {
    let ctx = document.getElementById("elementos_Chart").getContext('2d');
    elementos_Chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dataset.time,
            datasets: [
                {
                    label: 'Agua',
                    data: dataset.agua,
                    borderColor: "#8ccd56",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Metano',
                    data: dataset.metano,
                    borderColor: "#0213a2",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Etano',
                    data: dataset.etano,
                    borderColor: "#00a2a0",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Propano',
                    data: dataset.propano,
                    borderColor: "#a25900",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Butano',
                    data: dataset.butano,
                    borderColor: "#c2ca26",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Pentano',
                    data: dataset.pentano,
                    borderColor: "#a20406",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Hexano',
                    data: dataset.hexano,
                    borderColor: "#a200a1",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Nitrogeno',
                    data: dataset.nitrogeno,
                    borderColor: "#00a294",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Propano e Hidrocarburos superiores',
                    data: dataset.propano_e_hidrocarburos_superiores,
                    borderColor: "#587919",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Hexano Hydrocarburos',
                    data: dataset.hexano_hydrocarburos,
                    borderColor: "#5000a2",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Hidrogeno',
                    data: dataset.hidrogeno,
                    borderColor: "#486300",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Monoxido Carobono',
                    data: dataset.monoxido_carobono,
                    borderColor: "#355944",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Porcentaje vol Gas',
                    data: dataset.porcentaje_vol_gas,
                    borderColor: "#91a213",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }
            ]
        },
        options: {
            responsive: true,
            hover: {
                mode: 'nearest',
                intersect: true
            },

            legend: {
                position: 'top',

                labels: {
                    display: true,
                    boxWidth: 20,
                    padding: 25,
                    fontColor: '#000000',
                }
            },

            scales: {
                xAxes: [{
                    display: true,
                    categoryPercentage: 0.3,
                    barPercentage: 0.4,
                    ticks: {
                        display: true,
                        fontColor: '#000000',
                        padding: 10
                    }
                }]
            }
        }
    });
    return elementos_Chart
}

function create_chart_indices() {
    let ctx = document.getElementById("indices_Chart").getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: dataset.time,
            datasets: [
                {
                    label: 'Poder Calorifico Superior',
                    data: dataset.poder_calorifico_superior,
                    borderColor: "#8ccd56",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Poder Calorifico Inferior',
                    data: dataset.poder_calorifico_inferior,
                    borderColor: "#0213a2",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Indice Wobbe',
                    data: dataset.indice_wobbe,
                    borderColor: "#00a2a0",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Densidad Relativa',
                    data: dataset.densidad_relativa,
                    borderColor: "#a25900",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Gases Inertes Pmol',
                    data: dataset.gases_inertes_pmol,
                    borderColor: "#c2ca26",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Punto Rocio Hydrocarburos',
                    data: dataset.punto_rocio_hydrocarburos,
                    borderColor: "#a20406",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Resultado Odorizacion',
                    data: dataset.resultado_odorizacion,
                    borderColor: "#a200a1",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }, {
                    label: 'Resultado Impurezas',
                    data: dataset.resultado_impurezas,
                    borderColor: "#00a294",
                    fill: false,
                    borderWidth: 2,
                    tension: 0
                }
            ]
        },
        options: {
            responsive: true,
            hover: {
                mode: 'nearest',
                intersect: true
            },

            legend: {
                position: 'top',

                labels: {
                    display: true,
                    boxWidth: 20,
                    padding: 25,
                    fontColor: '#000000',
                }
            },

            scales: {
                xAxes: [{
                    display: true,
                    categoryPercentage: 0.3,
                    barPercentage: 0.4,
                    ticks: {
                        display: true,
                        fontColor: '#000000',
                        padding: 10
                    }
                }]
            }
        }
    });
}

elementos_Chart = create_chart();
var indices_chart = create_chart_indices();


$('#reportes-form').submit(function (event) {
    event.preventDefault();
    let form_data = $('#reportes-form').serializeArray();
    let posting = $.post(location.href, form_data);
    posting.done(function(data){
        if (data['error']) {
            alert(data['error'])
        } else {
            UpdateData(data, dataset, elementos_Chart, indices_chart);
        }
    });
});

function UpdateData(data, dataset, elementos_Chart) {
    dataset.time = data.fecha_muestra.map((el)=>(el));
    dataset.agua = data.elementos.agua.map((el)=>(el));
    dataset.metano = data.elementos.metano.map((el)=>(el));
    dataset.etano = data.elementos.etano.map((el)=>(el));
    dataset.propano = data.elementos.propano.map((el)=>(el));
    dataset.butano = data.elementos.butano.map((el)=>(el));
    dataset.pentano = data.elementos.pentano.map((el)=>(el));
    dataset.hexano = data.elementos.hexano.map((el)=>(el));
    dataset.nitrogeno = data.elementos.nitrogeno.map((el)=>(el));
    dataset.propano_e_hidrocarburos_superiores = data.elementos.propano_e_hidrocarburos_superiores.map((el)=>(el));
    dataset.hexano_hydrocarburos = data.elementos.hexano_hydrocarburos.map((el)=>(el));
    dataset.hidrogeno = data.elementos.hidrogeno.map((el)=>(el));
    dataset.monoxido_carobono = data.elementos.monoxido_carobono.map((el)=>(el));
    dataset.porcentaje_vol_gas = data.elementos.porcentaje_vol_gas.map((el)=>(el));
    dataset.poder_calorifico_superior = data.indices.poder_calorifico_superior.map((el)=>(el));
    dataset.poder_calorifico_inferior = data.indices.poder_calorifico_inferior.map((el)=>(el));
    dataset.indice_wobbe = data.indices.indice_wobbe.map((el)=>(el));
    dataset.densidad_relativa = data.indices.densidad_relativa.map((el)=>(el));
    dataset.gases_inertes_pmol = data.indices.gases_inertes_pmol.map((el)=>(el));
    dataset.punto_rocio_hydrocarburos = data.indices.punto_rocio_hydrocarburos.map((el)=>(el));
    dataset.resultado_odorizacion = data.indices.resultado_odorizacion.map((el)=>(el));
    dataset.resultado_impurezas = data.indices.resultado_impurezas.map((el)=>(el));
    elementos_Chart.destroy();
    indices_chart.destroy();
    indices_chart = create_chart_indices();
    create_chart();
}
