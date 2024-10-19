document.getElementById('process-btn').addEventListener('click', async () => {
    const fileInput = document.getElementById('upload');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please upload an image.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
    });

    const data = await response.json();

    if (data.error) {
        alert(data.error);
    } else {
        document.getElementById('denoised-image').src = data.denoised_image_url;
    }
});
