function handleImagePreview(input) {
    const wrapper = input.closest('.image-upload-wrapper');
    const placeholder = wrapper.querySelector('.upload-placeholder');
    const previewContainer = wrapper.querySelector('.preview-container');
    const previewImage = wrapper.querySelector('.img-preview');
  
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        previewImage.src = e.target.result;
        placeholder.classList.add('d-none');
        previewContainer.classList.remove('d-none');
      }
      reader.readAsDataURL(input.files[0]);
    }
  }
  
  function removeImage(btn, inputId) {
    const input = document.getElementById(inputId);
    input.value = '';
    const wrapper = btn.closest('.image-upload-wrapper');
    wrapper.querySelector('.preview-container').classList.add('d-none');
    wrapper.querySelector('.upload-placeholder').classList.remove('d-none');
  }
  
  function resetPreviews() {
    setTimeout(() => {
      document.querySelectorAll('.preview-container').forEach(el => el.classList.add('d-none'));
      document.querySelectorAll('.upload-placeholder').forEach(el => el.classList.remove('d-none'));
    }, 10);
  }