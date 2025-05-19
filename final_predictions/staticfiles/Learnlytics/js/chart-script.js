// static/Learnlytics/js/chart-script.js

const ctx = document.getElementById('predictionChart').getContext('2d');
const predictionChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Student A', 'Student B', 'Student C', 'Student D'],
        datasets: [{
            label: 'Predicted Grade',
            data: [85, 70, 95, 60],
            backgroundColor: [
                'rgba(93, 135, 255, 0.7)',
                'rgba(93, 200, 255, 0.7)',
                'rgba(93, 255, 135, 0.7)',
                'rgba(255, 173, 93, 0.7)'
            ],
            borderColor: [
                'rgba(93, 135, 255, 1)',
                'rgba(93, 200, 255, 1)',
                'rgba(93, 255, 135, 1)',
                'rgba(255, 173, 93, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});
