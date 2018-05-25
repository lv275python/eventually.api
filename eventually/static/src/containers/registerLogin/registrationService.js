import axios from 'axios';
import {apiUrl} from 'src/helper';

const appPath = apiUrl + 'user/',
    loginUrl = appPath + 'login/',
    logoutUrl = appPath + 'logout/',
    registerUrl = appPath + 'register/',
    forgetPasswordUrl = appPath + 'forget_password/';

const registerService = (email, password) => {
    return axios.post(registerUrl, {email, password}).catch(function (error) {
        if (error.request) {
            return error.request;
        }
    });
};

const loginService = (email, password) => {
    return axios.post(loginUrl, {email, password}).catch(function (error) {
        if (error.request) {
            return error.request;
        }
    });
};

const logoutService = () => {
    return axios.get(logoutUrl);
};

const forgetPasswordService = email => {
    return axios.post(forgetPasswordUrl, {email}).catch(function (error) {
        if (error.request) {
            return error.request.status;
        }
    });
};

const putNewPasswordService = (token, newPassword) => {
    return axios.put(forgetPasswordUrl+token, {'new_password' : newPassword}).catch(function (error) {
        if (error.request) {
            return error.request.status;
        }
    });
};

export {loginService, forgetPasswordService, registerService, logoutService, putNewPasswordService};
