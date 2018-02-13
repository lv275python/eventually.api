import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import EditEventTaskDialog from './EditEventTaskDialog';
import {Link} from 'react-router';
import Task from '../taskItem/Task';
import {deleteTeamService} from 'src/containers/event/EventService';


export default class EventTaskItem extends React.Component {
    handleDelete = () => {
        deleteTeamService(this.state.eventId, this.state.id);
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
                <Card>
                    <CardHeader
                        title={this.state.title}
                        actAsExpander={true}
                        showExpandableButton={true}
                    />
                    <CardActions>
                        <EditEventTaskDialog
                            title={this.state.title}
                            description={this.state.description}
                            members={this.props.members}
                            id={this.props.id}
                            assignmentUsers={this.props.assignmentUsers}
                            eventId={this.props.eventId}
                        />
                        <Task
                            eventId={this.state.eventId}
                            taskId={this.props.id}
                        />
                        <RaisedButton label="Delete" onClick={this.handleDelete}/>
                    </CardActions>
                    <CardText expandable={true}>
                        {this.state.description}
                    </CardText>
                </Card>
            </div>
        );
    }
}

