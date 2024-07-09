document.addEventListener('DOMContentLoaded', (event) => {
    fetchNumber();
});

function fetchNumber() {
    fetch('http://127.0.0.1:5000/get_value')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const number = data.number;
            console.log(number);
            document.getElementById('number').innerText = number.toFixed(2);
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
        });
}
