function uploadImageForAnalyze() {
    var input = document.getElementById('imageInput');
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var imgElement = document.getElementById('originalImage');
            imgElement.src = e.target.result;
            imgElement.style.display = 'block'; // 确保图片显示出来

            var formData = new FormData();
            formData.append('image', input.files[0]);

            fetch('/analyze', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json()) // 服务器返回JSON格式的数据
            .then(data => {
                console.log('Analysis result:', data);
                displayAnalysisResults(data.result); // 假设result是嵌套在顶层的一个键
            })
            .catch(error => {
                console.error('Error:', error);
            });
        };
        reader.readAsDataURL(input.files[0]); // 读取文件并转换为base64编码的URL
    } else {
        alert('Please select an image file.');
    }
}

function findMaxKey(obj) {
    const max = Math.max(...Object.values(obj));
    for (let [key, value] of Object.entries(obj)) {
        if (value === max) {
            return key;
        }
    }
    return null; // 如果没有找到匹配项，返回null
}


function displayAnalysisResults(results) {
    var resultsContainer = document.getElementById('analysisResults');
    var resultsHtml = `
        <h3>Analysis Results</h3>
        <p><strong>Emotion:</strong> ${findMaxKey(results[0].emotion)}</p>
        <p><strong>Age:</strong> ${results[0].age}</p>
        <p><strong>Gender:</strong> ${findMaxKey(results[0].gender)}</p>
        <p><strong>Race:</strong> ${findMaxKey(results[0].race)}</p>
    `;
    resultsContainer.innerHTML = resultsHtml;
}

