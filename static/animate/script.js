function uploadImageForAnimation() {
    var input = document.getElementById('imageInput');
    var file = input.files[0];
    var originalImage = document.getElementById('originalImage');
    var processedImage = document.getElementById('processedImage');
    var originalTitle = document.getElementById('originalTitle');
    var processedTitle = document.getElementById('processedTitle');

    // 显示原图
    var reader = new FileReader();
    reader.onload = function(e) {
        originalImage.src = e.target.result;
        originalImage.style.display = 'block'; // 显示原图
        originalTitle.style.display = 'block'; // 显示原图标题
    };
    reader.readAsDataURL(file);

    // 使用FormData上传图片
    var formData = new FormData();
    formData.append('image', file);

    fetch('/animate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        var url = URL.createObjectURL(blob);
        processedImage.src = url;
        processedImage.style.display = 'block'; // 显示处理后的图像
        processedTitle.style.display = 'block'; // 显示处理后图像的标题
    })
    .catch(error => console.error('Error:', error));
}