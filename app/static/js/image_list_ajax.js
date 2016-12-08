function getImages() {
    var httpRequest = new XMLHttpRequest();
    var url = '/admin/imagelist/1';

    if (!httpRequest) {
        console.log("XMLHttpRequest is not supported.");
    } else {
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
                console.log("state" + httpRequest.readyState);
                if (httpRequest.status === 200) {
                    var imagelistElement = document.getElementById('image-list');
                    imagelistElement.innerHTML = httpRequest.responseText;
                } else {
                    console.log("Could not load images");
                }
            }
        };
        httpRequest.open('GET', url);
        httpRequest.send();
    }
}
