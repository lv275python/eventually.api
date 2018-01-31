import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import {eventTaskServicePut} from './EventTaskService';


export default class EditEventTaskDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: this.props.id,
            title: this.props.title,
            description: this.props.description,
            members:this.props.members,
            assignment:this.props.assignment_users
        };
    }


    handleChangeState = () => {
        let newOpenState = this.state.openDialog?false:true;
        this.setState({openDialog: newOpenState});
    };


    handleName = event => {
        this.setState({title: event.target.value});
    };

    handleDescription = event => {
        this.setState({description: event.target.value});
    };

    handleUsers = (event, index, values) => this.setState({'assignment': values});

    handleSave = event => {
        let data = {};
        if (this.state.title != this.props.title) data['title'] = this.state.title;
        if (this.state.description != this.props.description) data['description'] = this.state.description;
        let addUsers = [];
        let removeUsers = [];
        for (let i = 0; i < this.state.assignment.length; i++)
            if (this.props.assignment_users.indexOf(this.state.assignment[i]) == -1) addUsers.push(this.state.assignment[i]);
        for (let i = 0; i < this.props.assignment_users.length; i++)
            if (this.state.assignment.indexOf(this.props.assignment_users[i]) == -1) removeUsers.push(this.props.assignment_users[i]);
        if (this.state.assignment != this.props.assignment_users) {
            if (addUsers.length !== 0) data['add_users'] = addUsers;
            if (removeUsers.length !== 0) data['remove_users'] = removeUsers;
        }
        eventTaskServicePut(this.props.eventId, this.state.id, data);
        this.props.handleDialogClose;
    };

    render() {
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.props.handleDialogClose}
            />,
            <FlatButton
                label="Save"
                primary={true}
                onClick={this.handleSave}
            />,
        ];
        return (
            <Dialog
                title="Task Edit"
                actions={actions}
                modal={false}
                open={this.props.open}
                autoDetectWindowHeight={true}
                onRequestClose={this.props.handleDialogClose}
            >
                <div>
                    <TextField
                        hintText="Task Title"
                        floatingLabelText="Enter name of the task"
                        defaultValue={this.state.title}
                        fullWidth={true}
                        onChange={this.handleName}
                    />
                </div>
                <div>
                    <TextField
                        hintText="Description"
                        floatingLabelText="Enter description of the task"
                        defaultValue={this.state.description}
                        fullWidth={true}
                        onChange={this.handleDescription}
                    />
                </div>
                <div>
                    <SelectField
                        multiple={true}
                        floatingLabelText="Select an assignment user(s)"
                        hintText="Assignment users"
                        value={this.state.assignment}
                        onChange={this.handleUsers}
                    >
                        {this.state.members.map((member) => (
                            <MenuItem
                                key={member.id}
                                insetChildren={true}
                                checked={this.state.assignment && this.state.assignment.indexOf(member.id) > -1}
                                value={member.id}
                                primaryText={member.full_name}
                            />
                        ))}
                    </SelectField>
                </div>
            </Dialog>
        );
    }
}
