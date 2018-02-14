import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import { Card, CardHeader, CardActions, CardText } from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import Paper from 'material-ui/Paper';
import EditEventTaskDialog from './EditEventTaskDialog';
import Task from '../taskItem/Task';
import {deleteTaskService} from 'src/containers/event/EventService';


export default class EventTaskItem extends React.Component {
    handleDelete = () => {
        deleteTaskService(this.state.eventId, this.state.id);
    }

    constructor(props) {
        super(props);
        this.state = {
            id: this.props.id,
            eventId: this.props.eventId,
            title: this.props.title,
            description: this.props.description.slice(0, 300) + '...',
            openDialog: false
        };
    }

    render() {
        return (
            <div>
                <Paper zDepth={3}>
                    <Card>
                        <CardHeader
                            title={this.state.title}
                            actAsExpander={true}
                            showExpandableButton={true}
                        />
                        <CardActions>
                            <Task
                                eventId = {this.state.eventId}
                                taskId = {this.props.id}
                            />
                            <EditEventTaskDialog
                                title = {this.state.title}
                                description = {this.state.description}
                                members = {this.props.members}
                                id = {this.props.id}
                                assignmentUsers = {this.props.assignmentUsers}
                                eventId = {this.props.eventId}
                            />
                            <RaisedButton label="Delete" onClick={this.handleDelete} style = {{margin: '1%'}}/>
                        </CardActions>
                        <CardText expandable={true}>
                            {this.state.description}
                        </CardText>
                    </Card>
                </Paper>
            </div>
        );
    }
}

