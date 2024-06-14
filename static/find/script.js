function uploadImageForDataBaseFind() {
    var input = document.getElementById('imageInput');
    var file = input.files[0];
    var originalImage = document.getElementById('originalImage');
    var processedImage = document.getElementById('processedImage');
    var originalTitle = document.getElementById('originalTitle');
    var processedTitle = document.getElementById('processedTitle');
    var verificationResult = document.getElementById('verificationResult');

    // // 显示原图
    // var reader = new FileReader();
    // reader.onload = function(e) {
    //     originalImage.src = e.target.result;
    //     originalImage.style.display = 'block'; // 显示原图
    //     originalTitle.style.display = 'block'; // 显示原图标题
    // };
    // reader.readAsDataURL(file);

    // // 使用FormData上传图片
    var formData = new FormData();
    formData.append('image', file);

    fetch('/find', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // 显示相似图像和distance值
            originalImage.src = 'data:image/jpeg;base64,' + data.original_image;
            originalImage.style.display = 'block'; // 显示原图
            originalTitle.style.display = 'block'; // 显示原图标题

            processedImage.src = 'data:image/jpeg;base64,' + data.db_image;
            processedImage.style.display = 'block'; // 显示处理后的图像
            processedTitle.style.display = 'block'; // 显示处理后图像的标题

            verificationResult.textContent = 'Distance: ' + data.distance;
            verificationResult.style.display = 'block'; // 显示验证结果
        }
    })
    .catch(error => console.error('Error:', error));
}