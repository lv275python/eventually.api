import {apiUrl} from 'src/helper';
import axios from 'axios';

const requestPath = apiUrl + 'upload/';
const requestTimeout = 30000;

const sendFile = (data, type) => {
    let url;
    if (type === 'img'){
        url = requestPath + 'img_handle/';
    } else {
        url = requestPath + 'doc_handle/';
    }
    return axios.post(url, data, {timeout: requestTimeout});
};

const deleteFile = imageName => {
    return axios.delete(requestPath, {
        headers: {'Content-Type': 'application/json'},
        timeout: requestTimeout,
        data: {
            'image_key': imageName
        }
    });
};



export {sendFile, deleteFile};
