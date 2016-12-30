var page_number = 1;

function getImages() {
    var httpRequest = new XMLHttpRequest();
    var url = '/admin/imagelist/' + page_number;

    if (!httpRequest) {
        console.log("XMLHttpRequest is not supported.");
    } else {
        httpRequest.onreadystatechange = function () {
            if (httpRequest.readyState === XMLHttpRequest.DONE) {
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

function updateNumber(button) {
    if (button.id === "previous") {
        page_number -= 1;
        if (page_number < 1) {
            page_number = 1;
        }
    } else {
        page_number += 1;
    }
    getImages();
}

// Doesn't work with AJAX but maybe use html data atribute.
function getPageNumber() {
    var pageNumberElement = document.getElementById("page_number_id");
    if (pageNumberElement === null) {
        return;
    }
    pageNumberElement.text("Page " + page_number + "/");
}

// Wait for the '#page_number_id' element to load.
setTimeout(function () {}, 500);
getPageNumber();
