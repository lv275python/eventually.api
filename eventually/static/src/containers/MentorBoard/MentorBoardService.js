import axios from 'axios';
import {apiUrl} from 'src/helper';

const assigmentMentorPath = apiUrl + 'assignment/mentor/';

const getCurriculumsService = () => {
    let url = assigmentMentorPath + 'curriculum/';
    return axios.get(url);
};

export {getCurriculumsService} ;
