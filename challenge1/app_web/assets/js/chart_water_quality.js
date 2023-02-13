// render water quality chart
const waterQualityChart = new ApexCharts(document.querySelector("#chart-water-quality"), {
    title: {
        text: 'Water Quality',
        align: 'left'
    },
    chart: {
        height: 350,
        type: 'pie',
    },
    series: [],
    labels: [],
    colors: ['#00E396', '#FF4560'],
    tooltip: {
        x: {
            show: false
        },
        y: {
            formatter: function (value) {
                return value.toLocaleString();
            }
        }
    },
});
waterQualityChart.render();

// fetch the data asynchronously
fetch("/assets/data/water-quality.json").then(response => {
    response.json().then(data => {
        waterQualityChart.updateSeries(data.data);
        waterQualityChart.updateOptions({ labels: data.index });
    });
});
