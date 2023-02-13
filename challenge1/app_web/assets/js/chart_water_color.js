// render water color chart
const waterColorChart = new ApexCharts(document.querySelector("#chart-water-color"), {
    title: {
        text: 'Water Color',
        align: 'left'
    },
    chart: {
        height: 350,
        type: 'pie',
    },
    series: [],
    labels: [],
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
waterColorChart.render();

// fetch the data asynchronously
fetch("/assets/data/water-color.json").then(response => {
    response.json().then(data => {
        waterColorChart.updateSeries(data.data);
        waterColorChart.updateOptions({ labels: data.index });
    });
});
