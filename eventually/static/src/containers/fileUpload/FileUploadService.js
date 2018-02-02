import {apiUrl} from 'src/helper';
import axios from 'axios';

const request_path = apiUrl + 'img/handle/';
const request_timeout = 30000;

const sendFile = data => {
    return axios.post(request_path, data, {timeout: request_timeout});
};

export {sendFile};
