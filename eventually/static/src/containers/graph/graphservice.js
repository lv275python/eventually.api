import axios from 'axios';
import { apiUrl } from 'src/helper';

const assUrl = apiUrl + 'assignment/answer/';

export const getAssignments = () => {
    return axios.get(assUrl);
};
