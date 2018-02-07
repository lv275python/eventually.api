import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import Dialog from 'material-ui/Dialog';
import {Link} from 'react-router';
import {getTask} from './TaskService';
const STATUS_CHOICES = {
    0: 'ToDo',
    1: 'In Progress',
    2: 'Done',
};

const liStyle ={
    margin: '20px 20px',
    fontSize: '19px',
    fontFamily: 'Roboto, sans-serif',
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
class Task extends React.Component {

    constructor(props) {

        super(props);
        this.state = {
            id: this.props.taskId,
            team: '',
            name: '',
            description: '',
            created_at: '',
            updated_at: '',
            event_id: this.props.eventId,
            users:[],
            open: false
        };
    }


    componentWillMount() {
        this.getDataTask();

    }

    handleDialogOpen = () =>{
        this.setState({'open': true});
    }

    handleDialogClose = () =>{
        this.setState({'open': false});
    }

    getDataTask=()=>{
        getTask(this.state.event_id,this.state.id, true).then(response => {
            this.setState({
                Title: response.data['title'],
                description: response.data['description'],
                created_at: response.data['created_at'],
                updated_at: response.data['updated_at'],
                status: response.data['status'],
                users: response.data['users_id']

            });
        });
    }
    render(){
        const actions = [
            <RaisedButton
                label="Ok"
                primary={true}
                onClick={this.handleDialogClose}
            />,
        ];
        return (
            <div >
                <RaisedButton label="Details" onClick = {this.handleDialogOpen} />
                <div style={styleLowerMain1}>
                   {this.state.open &&
                       <Dialog
                            title="Task Details"
                            actions={actions}
                            modal={false}
                            open={this.state.open}
                            onRequestClose={this.handleDialogClose}
                       >
                            <div>
                                <p style={styleInp}><span style={styleSpan}>Title :</span>{this.state.Title}</p>
                                <p style={styleInp}><span style={styleSpan}>Description :</span>{this.state.description}</p>
                                <p style={styleInp}><span style={styleSpan}>Created at :</span>{(new Date(this.state.created_at*1000)).toDateString()}</p>
                                <p style={styleInp}><span style={styleSpan}>Updated at :</span>{(new Date(this.state.updated_at*1000)).toDateString()}</p>
                                <p style={styleInp}><span style={styleSpan}>Status :</span>{STATUS_CHOICES [this.state.status]}</p>
                                <p style={styleInp}><span style={styleSpan}>Users :</span></p>
                                <ul key='0'>
                                    {
                                        console.log(this.state.users),
                                        this.state.users.map(usr => <li key={usr['id']} style={liStyle}>{usr['first_name']+'  '+usr['last_name']}</li>)
                                    }
                           </ul>
                           </div>
                       </Dialog>
                   }
                </div>
            </div>
        );
    }
}

export default Task;
