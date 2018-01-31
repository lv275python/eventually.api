import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import {eventTaskServicePost, taskGetTeamService} from './EventTaskService';


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
            status: 0,
            eventId: props.eventId,
            teamId: props.teamId,
            members: [],
            assignment: []
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
        this.setState({ open: false });
    };

    handleTitle = event => {
        this.setState({title: event.target.value});
    };

    handleDescription = event => {
        this.setState({description: event.target.value});
    };

    handleStatus = (event, index, value) => {
        this.setState({'status': value});
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
        const data = {
            'title': this.state.title,
            'description': this.state.description,
            'status': this.state.status,
            'users': this.state.values
        };
        eventTaskServicePost(this.state.eventId, data).then(response => {
            this.handleClose();
        });
    };

    render() {
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleSubmit}
            />,
        ];
        const {values} = this.state;
        return (
            <div>
                <FloatingActionButton
                    onClick={this.handleOpen}
                    style={FlatButtonStyle}>
                    <ContentAdd />
                </FloatingActionButton>
                <Dialog
                    title={this.props.title}
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                >
                    <TextField
                        hintText="Name"
                        fullWidth={true}
                        onChange = {this.handleTitle} />
                    <TextField
                        hintText="Description"
                        onChange = {this.handleDescription}
                        multiLine={true}
                        rows={2}
                        rowsMax={4}
                        fullWidth={true} />
                    <SelectField
                        floatingLabelText="Status"
                        fullWidth={true}
                        value={this.state.status}
                        onChange = {this.handleStatus}
                    >
                        <MenuItem value = {0} primaryText = 'To do' />
                        <MenuItem value = {1} primaryText = 'In Progress' />
                        <MenuItem value = {2} primaryText = 'Done' />
                    </SelectField>
                    <SelectField
                        multiple={true}
                        floatingLabelText="Select users"
                        value={this.state.assignment}
                        onChange={this.handleChange}
                        // selectionRenderer={this.selectionRenderer}
                    >
                        {this.menuItems(this.state.members)}
                    </SelectField>
                </Dialog>
            </div>
        );
    }
}
