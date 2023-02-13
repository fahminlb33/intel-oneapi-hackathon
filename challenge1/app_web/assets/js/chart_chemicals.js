// render chemical time series chart
const chemicalChart = new ApexCharts(document.querySelector("#chart-chemicals"), {
    title: {
        text: '',
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
            text: 'Concentration'
        },
    },
    series: [],
    dataLabels: {
        enabled: false
    },
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
chemicalChart.render();

// set minimum checkbox
const minCheckbox = document.querySelector("#scale-to-zero");
minCheckbox.addEventListener("change", (e) => {
    chemicalChart.updateOptions({
        yaxis: {
            min: e.target.checked ? 0 : undefined,
            max: e.target.checked ? (v) => v + v * 0.2 : undefined
        }
    });
});

// fetch the data asynchronously
fetch("/assets/data/water-chemicals.json").then(response => {
    response.json().then(data => {
        const series = [
            {
                name: 'pH',
                data: Object.keys(data).map((d) => [+d, data[d].ph])
            },
            {
                name: 'Fluoride',
                data: Object.keys(data).map((d) => [+d, data[d].fluoride])
            },
            {
                name: 'Iron',
                data: Object.keys(data).map((d) => [+d, data[d].iron])
            },
            {
                name: 'Copper',
                data: Object.keys(data).map((d) => [+d, data[d].copper])
            },
            {
                name: 'Nitrate',
                data: Object.keys(data).map((d) => [+d, data[d].nitrate])
            },
            {
                name: 'Sulfate',
                data: Object.keys(data).map((d) => [+d, data[d].sulfate])
            },
            {
                name: 'Chloride',
                data: Object.keys(data).map((d) => [+d, data[d].chloride])
            },
            {
                name: 'Chlorine',
                data: Object.keys(data).map((d) => [+d, data[d].chlorine])
            },
            {
                name: 'Lead',
                data: Object.keys(data).map((d) => [+d, data[d].lead])
            },
            {
                name: 'Manganese',
                data: Object.keys(data).map((d) => [+d, data[d].manganese])
            },
            {
                name: 'Zinc',
                data: Object.keys(data).map((d) => [+d, data[d].zinc])
            },
            {
                name: 'Odor',
                data: Object.keys(data).map((d) => [+d, data[d].odor])
            }
        ];

        chemicalChart.updateSeries([series[0]]);

        const chemicalSelect = document.querySelector("#chart-chemical-series");
        chemicalSelect.addEventListener("change", (e) => {
            chemicalChart.updateSeries([series.find((s) => s.name === e.target.value)]);
        });
    });
});
