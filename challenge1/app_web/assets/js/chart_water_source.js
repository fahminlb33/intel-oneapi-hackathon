// render water source chart
const waterSourceChart = new ApexCharts(document.querySelector("#chart-water-source"), {
    title: {
        text: 'Water Source',
        align: 'left'
    },
    chart: {
        height: 350,
        type: 'pie',
    },
    series: [],
    labels: [],
    theme: {
        monochrome: {
            enabled: true
        }
    },
    tooltip: {
        x: {
            show: false
        },
        y: {
            formatter: function (value) {
                return value.toLocaleString();
            },
        }
    },
});
waterSourceChart.render();

// fetch the data asynchronously
fetch("/assets/data/water-source.json").then(response => {
    response.json().then(data => {
        waterSourceChart.updateSeries(data.data);
        waterSourceChart.updateOptions({ labels: data.index });
    });
});
