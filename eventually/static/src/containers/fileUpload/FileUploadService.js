import {apiUrl} from 'src/helper';
import axios from 'axios';

const requestPath = apiUrl + 'img/handle/';
const requestTimeout = 30000;

const sendFile = data => {
    return axios.post(requestPath, data, {timeout: requestTimeout});
};

export {sendFile};
