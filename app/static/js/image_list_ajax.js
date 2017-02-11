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
    var previousElement = document.getElementById('previous');
    var amount_of_pages = previousElement.dataset.pagenumbers;
    if (button.id === "previous") {
        page_number -= 1;
        if (page_number < 1) {
            page_number = 1;
        }
    } else {
        if (amount_of_pages > page_number) {
            page_number += 1;
        }
    }
    getImages();
    getPageNumber(amount_of_pages);
}

// Doesn't work with AJAX but maybe use html data atribute.
function getPageNumber(amount_of_pages) {
    var page_number_idElement = document.getElementById('page_number_id');
    page_number_idElement.innerHTML = page_number + " / " + amount_of_pages;
}
