// render chemical time series chart
const physicalChart = new ApexCharts(document.querySelector("#chart-physical"), {
    title: {
        text: 'Physical Properties by Week',
        align: 'left'
    },
    chart: {
        height: 350,
        type: 'area',
    },
    xaxis: {
        type: 'datetime'
    },
    yaxis: {
        labels: {
            formatter: function (val) {
                return val.toFixed(4);
            },
        },
        title: {
            text: 'Value'
        }
    },
    series: [],
    dataLabels: {
        enabled: false
    },
});
physicalChart.render();

// fetch the data asynchronously
fetch("/assets/data/water-chemicals.json").then(response => {
    response.json().then(data => {
        const series = [
            {
                name: 'Turbidity',
                data: Object.keys(data).map((d) => [+d, data[d].turbidity])
            },
            {
                name: 'Conductivity',
                data: Object.keys(data).map((d) => [+d, data[d].conductivity])
            },
            {
                name: 'Total Dissolved Solids',
                data: Object.keys(data).map((d) => [+d, data[d].total_dissolved_solids])
            },
            {
                name: 'Air Temperature',
                data: Object.keys(data).map((d) => [+d, data[d].air_temperature])
            },
            {
                name: 'Turbidity',
                data: Object.keys(data).map((d) => [+d, data[d].water_temperature])
            }
        ];

        physicalChart.updateSeries(series);
    });
});
