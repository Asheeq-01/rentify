function handleImagePreview(input) {
    const wrapper = input.closest('.image-upload-wrapper');
    const placeholder = wrapper.querySelector('.upload-placeholder');
    const previewContainer = wrapper.querySelector('.preview-container');
    const previewImage = wrapper.querySelector('.img-preview');
  
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        previewImage.src = e.target.result;
        if(placeholder) placeholder.classList.add('d-none');
        previewContainer.classList.remove('d-none');
      }
      reader.readAsDataURL(input.files[0]);
    }
  }
  
  function removeImage(btn, inputId) {
    const input = document.getElementById(inputId);
    input.click(); // Trigger file selection instead of just clearing
  }