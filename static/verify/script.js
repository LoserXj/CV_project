function uploadImagesForVerification() {
    var input1 = document.getElementById('imageInput1');
    var input2 = document.getElementById('imageInput2');
    var file1 = input1.files[0];
    var file2 = input2.files[0];

    var originalImage1 = document.getElementById('originalImage1');
    var originalImage2 = document.getElementById('originalImage2');
    var originalTitle1 = document.getElementById('originalTitle1');
    var originalTitle2 = document.getElementById('originalTitle2');
    var verificationResult = document.getElementById('verificationResult');

    // 显示原图1
    var reader1 = new FileReader();
    reader1.onload = function(e) {
        originalImage1.src = e.target.result;
        originalImage1.style.display = 'block'; // 显示原图1
        originalTitle1.style.display = 'block'; // 显示原图1标题
    };
    reader1.readAsDataURL(file1);

    // 显示原图2
    var reader2 = new FileReader();
    reader2.onload = function(e) {
        originalImage2.src = e.target.result;
        originalImage2.style.display = 'block'; // 显示原图2
        originalTitle2.style.display = 'block'; // 显示原图2标题
    };
    reader2.readAsDataURL(file2);

    // 使用FormData上传图片
    var formData = new FormData();
    formData.append('image1', file1);
    formData.append('image2', file2);

    fetch('/verify', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        verificationResult.textContent = 'Verification Result: ' + data.result + '\nDistance: ' + data.distance;
        verificationResult.style.display = 'block'; // 显示验证结果
    })
    .catch(error => console.error('Error:', error));
}