import axios from 'axios';
import {apiUrl} from 'src/helper';

const assigmentMentorPath = apiUrl + 'assignment/mentor/';

const getCurriculumsService = () => {
    let url = assigmentMentorPath + 'curriculum/';
    return axios.get(url);
};

const checkUserAnswer = (id, grade) => {
    const data = {
        id, grade
    };
    console.log(grade);
    let url = assigmentMentorPath + id;
    return axios.put(url, data);
};

const dismissUserAnswer = (id, status) => {
    const data = {
        id, status
    };
    let url = assigmentMentorPath + id;
    return axios.put(url, data);
};

const sendAnswerToUser = (message, userId) => {
    let url = assigmentMentorPath + 'send_answer/';
    let data = {
        message, userId
    };
    return axios.post(url, data);
};

export {getCurriculumsService, checkUserAnswer, dismissUserAnswer, sendAnswerToUser} ;
