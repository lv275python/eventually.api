import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import {Card, CardHeader, CardActions, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import EditEventTaskDialog from './EditEventTaskDialog';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
export default class EventTaskItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            goToTask:this.props.goToTask,
            title: this.props.title,
            description: this.props.description.slice(0,300)+'...',
            openDialog: false
        };
    }

    handleDialogOpen = () =>{
        this.setState({'openDialog': true});
    }

    handleDialogClose = () =>{
        this.setState({'openDialog': false});
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
                        <FlatButton label="Edit" onClick={this.handleDialogOpen}/>
                        <FlatButton label="Details" onClick={()=>this.state.goToTask(this.props.id)}/>
                    </CardActions>
                    <CardText expandable={true}>
                        {this.state.description}
                    </CardText>
                </Card>
                <EditEventTaskDialog
                    open = {this.state.openDialog}
                    title = {this.state.title}
                    description = {this.state.description}
                    members = {this.props.members}
                    id = {this.props.id}
                    assignment_users = {this.props.assignment_users}
                    handleDialogClose = {this.handleDialogClose}
                    eventId = {this.props.eventId}
                />
            </div>
        );
    }
}

