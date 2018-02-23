import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import { eventTaskServicePost, taskGetTeamService } from './EventService';


const FlatButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

export default class TaskDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            title: '',
            description: '',
            eventId: props.eventId,
            teamId: props.teamId,
            members: [],
            assignment: [],
            messageTitle: '',
            titleIsValid: false,
        };
    }

    componentWillMount() {
        taskGetTeamService(this.state.teamId, true).then(response => {
            this.setState({'members': response.data['members_id']});
        });
    }

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({
            open: false,
            messageTitle: '',
            titleIsValid: false,
            assignment: []
        });
    };

    handleTitle = event => {
        const regex = /^.{4,255}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                messageTitle: '',
                title: event.target.value,
                titleIsValid: true,
            });
        } else {
            this.setState({
                messageTitle: 'Required a minimum length of 4 characters',
                titleIsValid: false,
            });
        }
    };

    handleDescription = event => {
        this.setState({description: event.target.value});
    };

    handleChange = (event, index, values) => this.setState({'assignment': values});

    menuItems(values) {
        return this.state.members.map((member) => (
            <MenuItem
                key={member.id}
                insetChildren={true}
                checked={values && this.state.assignment.indexOf(member.id) > -1}
                value={member.id}
                primaryText={member.first_name + ' ' + member.last_name}
            />
        ));
    }

    handleSubmit = () => {
        if(this.state.titleIsValid === true){
            const data = {
                'title': this.state.title,
                'description': this.state.description,
                'users': this.state.assignment
            };
            eventTaskServicePost(this.state.eventId, data).then(response => {
                this.handleClose();
            });
        }
    };

    render() {
        const disable = !this.state.titleIsValid;
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                onClick={this.handleSubmit}
                disabled={disable}
            />,
        ];
        return (
            <div>
                <FloatingActionButton
                    onClick={this.handleOpen}
                    style={FlatButtonStyle}>
                    <ContentAdd />
                </FloatingActionButton>
                <Dialog
                    title="Add task"
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                >
                    <TextField
                        hintText="Name"
                        fullWidth={true}
                        onChange={this.handleTitle}
                        errorText={this.state.messageTitle} />
                    <TextField
                        hintText="Description"
                        onChange={this.handleDescription}
                        multiLine={true}
                        rowsMax={4}
                        fullWidth={true} />
                    <SelectField
                        multiple={true}
                        floatingLabelText="Select users"
                        value={this.state.assignment}
                        onChange={this.handleChange}
                    >
                        {this.menuItems(this.state.members)}
                    </SelectField>
                </Dialog>
            </div>
        );
    }
}
