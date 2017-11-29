import axios from "axios"

const appPath = '/api/v1/user/'
const loginUrl = appPath + 'login/';
const logoutUrl = appPath + 'logout/';
const registerUrl = appPath + 'register/';
const forgetPasswordUrl = appPath + 'forget_password/'

const registerService = (email, password) => {
    return axios.post(registerUrl, {email, password} );
}

const loginService = (email, password) => {
  return axios.post(loginUrl, {email, password} );
}

const logoutService = () => {
  return axios.get(logoutUrl);
}

const forgetPasswordService = email =>  {
  return axios.post(forgetPasswordUrl, {email} );
}

export { loginService, forgetPasswordService, registerService, logoutService }
