function previewCover(file) {
    if (file.files && file.files[0])
    {
        var reader = new FileReader();
        reader.onload = function(evt){
            document.getElementById('video-cover-preview').setAttribute("src",evt.target.result);
        }
        reader.readAsDataURL(file.files[0]);
    }
}
function submitCover(rec)
{
    var files = $('input[name="upload-video-cover"]').prop('files');
    if (files.length == 0) {
        alert("Please choose an image");
        return false;
    }
    var file = files[0];
    if(!/image\/\w+/.test(file.type)){
        alert("The file should be an image");
        return false;
    }
    var reader = new FileReader();
    var data;
    reader.readAsArrayBuffer(file);
    reader.onload = function(e){
        data = e.target.result;
        
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/video_cover/"+rec+"/", true);
        xhr.send(data);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                if (xhr.status == 200)
                    alert("Upload successfully");
                else
                    //document.getElementById("ccc").innerHTML = xhr.response;
                    alert("Failed uploading");
            }
        }
    }
}

