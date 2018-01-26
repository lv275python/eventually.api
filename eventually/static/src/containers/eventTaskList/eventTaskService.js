import axios from 'axios';

const eventPath = '/api/v1/events/';
const taskPath = '/api/v1/task/';

const eventTasksServiceGet = event_id => {
    return axios.get(eventPath+event_id+'/tasks/');
};

const eventServiceGet = event_id => {
    return axios.get(eventPath+event_id+'/');
};

const eventTaskServicePut = (task_id, status) => {
    return axios.put(taskPath + task_id + '/', {'status': +status});
};

export {eventTasksServiceGet, eventServiceGet, eventTaskServicePut};

