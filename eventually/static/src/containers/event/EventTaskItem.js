import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import { Card, CardHeader, CardActions, CardText } from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import EditEventTaskDialog from './EditEventTaskDialog';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import Task from '../taskItem/Task';


export default class EventTaskItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.eventId,
            title: this.props.title,
            description: this.props.description.slice(0,300)+'...',
            openDialog: false
        };
    }

    render() {
        return (
            <div>
                <Card>
                    <CardHeader
                        title={this.state.title}
                        actAsExpander={true}
                        showExpandableButton={true}
                    />
                    <CardActions>
                        <EditEventTaskDialog
                            title = {this.state.title}
                            description = {this.state.description}
                            members = {this.props.members}
                            id = {this.props.id}
                            assignmentUsers = {this.props.assignmentUsers}
                            eventId = {this.props.eventId}
                        />
                        <Task
                            eventId = {this.state.eventId}
                            taskId = {this.props.id}
                        />
                    </CardActions>
                    <CardText expandable={true}>
                        {this.state.description}
                    </CardText>
                </Card>
            </div>
        );
    }
}

