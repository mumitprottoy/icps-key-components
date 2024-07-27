
const previewImage = () => {
    const previewer = document.getElementById('previewer');
    const imageFile = document.getElementById('image-input').files[0];
    const imageUrlInput = document.getElementById('image-url-input');
    const reader = new FileReader();
    reader.readAsDataURL(imageFile);

    reader.addEventListener('load', ()=> {
        previewer.src = reader.result;
        previewer.style.display='block';
        imageUrlInput.value = reader.result;
    }, false)
}