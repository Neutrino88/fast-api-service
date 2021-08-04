// Element id, inside of which there will be a preview of the uploaded image on the index page
const imagePreviewParentId = 'imagePreviewParentId';
// Variable which will store image
let imageFileReader = null;
// URLs
const serverUrl = 'http://localhost:8000';
const sendImageUrl = serverUrl + '/negative_image';
const getLastImagesUrl = serverUrl + '/get_last_images';

// Encode image to base64
function encodeImageToBase64(element, callback) {
    const file = element.files[0];
    imageFileReader = new FileReader();
    imageFileReader.onloadend = function() {
        // print encoded image to console
        console.log('Encoded image: ', imageFileReader.result);
        callback(imageFileReader.result);
    };
    imageFileReader.readAsDataURL(file);
}

// OnChange image file
function onChangeFile(element) {
    encodeImageToBase64(element, function () {
        // preview loaded image
        removeElemContent(imagePreviewParentId);
        document.getElementById(imagePreviewParentId).innerText = 'Предпросмотр изображения';
        drawImage(imageFileReader.result, imagePreviewParentId);
    });
}

// Draw encoded image inside element with id = parent_elem_id
function drawImage(encoded_image, parent_elem_id, image_width=200) {
    const image = new Image();
    image.src = encoded_image;
    image.width = image_width;
    document.getElementById(parent_elem_id).appendChild(image);
}

// Remove all child on element with id = element_id
function removeElemContent(element_id) {
    document.getElementById(element_id).innerHTML = '';
}

// Send HTTP request
function sendRequest(method, url, headers, data, callback) {
    // print info
    console.log('sendRequest('+method+','+url+','+headers+','+data+','+callback+')');

    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    headers.forEach(function (header) { xhr.setRequestHeader(header[0], header[1]); });

    console.log(xhr);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let json = JSON.parse(xhr.responseText);
            console.log(json);
            callback(json);
        }
    };
    xhr.send(data);
}

// Send image to server
function sendImage() {
    if (imageFileReader === null) {
        console.log('SendImage(): imageFileReader is null');
        return;
    }
    const headers = [['Content-Type', 'application/json']];
    const data = JSON.stringify({'image': imageFileReader.result});

    sendRequest('POST', sendImageUrl, headers, data, function(json_data) {
        // get response with negative image
        console.log('SendImage() [response]:');
        console.log(json_data);

        // preview negative image
        removeElemContent(imagePreviewParentId);
        document.getElementById(imagePreviewParentId).innerText = 'Негатив изображения';
        drawImage(json_data['image'], imagePreviewParentId);
    });
}

// OnLoad view images page
function onLoadViewImagesPage() {
    sendRequest('GET', getLastImagesUrl, [], null, function(json_data) {
        // get response with last images
        console.log('getLastImages() [response]:');
        console.log(json_data);
        // show images
        if (json_data.length === 0) {
            console.log('json_data.length === 0');
        } else {
            json_data.forEach(function (pair) {
                createTableRow(pair['id'], pair['image'], pair['neg_image']);
            });
        }
        // show body element
        document.getElementById('containerId').style['visibility'] = 'visible';
    });
}

// Add to table original and negative images
function createTableRow(images_id, orig_img, neg_img, width=200) {
    const tr = document.createElement('tr');
    const td1 = document.createElement('td');
    const td2 = document.createElement('td');

    document.getElementById('tableId').appendChild(tr);
    tr.appendChild(td1);
    tr.appendChild(td2);

    td1.setAttribute('id', images_id + '_orig');
    drawImage(orig_img, images_id + '_orig', width);

    td2.setAttribute('id', images_id + '_neg');
    drawImage(neg_img, images_id + '_neg', width);
}
