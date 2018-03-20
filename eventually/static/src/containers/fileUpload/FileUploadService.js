import {apiUrl} from 'src/helper';
import axios from 'axios';

const requestPath = apiUrl + 'img/handle/';
const requestTimeout = 30000;

const sendFile = data => {
    return axios.post(requestPath, data, {timeout: requestTimeout});
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
