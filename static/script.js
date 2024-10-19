document.getElementById('upload-form').onsubmit = function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    
    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        const resultDiv = document.getElementById('result');
        const img = document.getElementById('restored-image');
        img.src = url;
        resultDiv.classList.remove('hidden');
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
};
