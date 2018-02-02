import React from 'react';
import {Link} from 'react-router';
import {getTask} from './TaskService';
import FlatButton from 'material-ui/FlatButton';
const STATUS_CHOICES = {
    0: 'ToDo',
    1: 'In Progress',
    2: 'Done',
};


const styleLowerMain1 = {
    display: 'flex',
    justifyContent: 'center',
    width: '100%',
    margin: '10px 10px',
};

const styleInp = {
    fontSize: '19px',
    fontFamily: 'Roboto, sans-serif',
};

const styleSpan = {
    display: 'inline-block',
    fontSize: '20px',
    fontFamily: 'Roboto, sans-serif',
    width: '117px',
};
class Event extends React.Component {

    constructor(props) {

        super(props);
        this.state = {

            id:'1', //this.props.match.params.taskId,
            team: '',
            name: '',
            description: '',
            created_at: '',
            updated_at: '',
            event_id: '1',//this.props.match.params.eventId,
            users:['user1','user',],
        };
    }


    componentWillMount() {
        this.getDataTask();

    }

    getDataTask=()=>{
        getTask(this.state.event_id,this.state.id, true).then(response => {
            this.setState({
                Title: response.data['title'],
                description: response.data['description'],
                created_at: response.data['created_at'],
                updated_at: response.data['updated_at'],
                status: response.data['status'],
                users: response.data['user']

            });
            console.log(response);
        });
    }
    render(){
        const user = userInf=>{
            return (
                <div>
                    {/*<li style={styleInp}>{userInf['first_name']}+''+{userInf['last_name']}</li>*/}
                    <li style={styleInp}>{userInf}</li>
                </div>
            );
        };
        return (
            <div >

                <div style={styleLowerMain1}>
                    <div>
                        <p style={styleInp}><span style={styleSpan}>Title :</span>{this.state.Title}</p>
                        <p style={styleInp}><span style={styleSpan}>Description :</span>{this.state.description}</p>
                        <p style={styleInp}><span style={styleSpan}>Created at :</span>{(new Date(this.state.created_at*1000)).toDateString()}</p>
                        <p style={styleInp}><span style={styleSpan}>Updated at :</span>{(new Date(this.state.updated_at*1000)).toDateString()}</p>
                        <p style={styleInp}><span style={styleSpan}>Status :</span>{STATUS_CHOICES [this.state.status]}</p>
                        <p style={styleInp}><span style={styleSpan}>Users :</span></p>
                        {this.state.users && <ul>
                            <p> something </p>
                         this.state.users.map(usr => user(usr));
                        </ul>
                        }
                    </div>
                </div>
            </div>
        );
    }
}

export default Event;
