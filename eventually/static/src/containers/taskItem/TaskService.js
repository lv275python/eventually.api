import axios from 'axios';
const rootUrl = '/api/v1/';
const eventPath = rootUrl + 'events/';


const getTask = (eventId, taskId, full_name) => {
    let url = eventPath + eventId + '/task/' + taskId + '/';
    if (full_name) url += '?full_name=true';
    return axios.get(url);
};
export { getTask };
