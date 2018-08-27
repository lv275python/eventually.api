export const s3Root='https://s3.eu-central-1.amazonaws.com/';

export function getImageUrl(imageName) {
    if (imageName) {
        return s3Root + 'eventually-img/' + imageName;
    }
}

export const isLogged = () => document.cookie.indexOf('sessionid') !== -1;

export const getUserId = () => {
    let cookies = document.cookie.split(';').map(cookie => cookie.replace(' ', ''));
    const name = 'user_id=';

    for (let i=0; i < cookies.length; i++) {
        if(cookies[i].indexOf(name) !== -1) {
            return +cookies[i].substring(name.length, cookies[i].length);
        }
    }
    return null;
};

export const apiUrl = '/api/v1/';

export const validatePassword = (password) => {
    const regexp = /^(?=.*[0-9])(?=.*[A-Z])[a-zA-Z0-9!@#$%^&*]{6,16}$/;
    return regexp.test(password);
};
