let chart;
let lastTimestamp = 0;
const maxDataPoints = 10;

function formatTime(date) {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let seconds = date.getSeconds();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;
    return hours + ':' + minutes + ':' + seconds + ' ' + ampm;
}


function updateNetworkStats() {
    const currentTime = Math.floor(Date.now() / 1000);
    const startTimestamp = lastTimestamp || currentTime - 120;
    const endTimestamp = currentTime - 60;

    fetch(`net.php?filename=log.csv&start=${startTimestamp}&end=${endTimestamp}`)
    .then(response => response.json())
    .then(dataArray => {
        if (dataArray.length === 0) {
            console.log("No new data available.");
            return;
        }

        dataArray = dataArray.filter(data => data.timestamp > lastTimestamp && data.timestamp <= endTimestamp);

        dataArray.forEach(data => {
            let date = new Date(data.timestamp * 1000);
            let formattedDate = formatTime(date);
            chart.data.labels.push(formattedDate);
            chart.data.datasets[0].data.push(data.downloadSpeed);
            chart.data.datasets[1].data.push(data.uploadSpeed);
            lastTimestamp = data.timestamp;
        });

        while (chart.data.labels.length > maxDataPoints) {
            chart.data.labels.shift();
            chart.data.datasets.forEach(dataset => {
                dataset.data.shift();
            });
        }

        chart.update();
    })
    .catch(error => console.error('Error:', error));
}

window.onload = function() {
    const ctx = document.getElementById('chart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Download Speed',
                backgroundColor: 'rgba(0, 123, 255, 0.5)',
                borderColor: 'rgba(0, 123, 255, 1)',
                data: []
            }, {
                label: 'Upload Speed',
                backgroundColor: 'rgba(40, 167, 69, 0.5)',
                borderColor: 'rgba(40, 167, 69, 1)',
                data: []
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
};

setInterval(updateNetworkStats, 5000);