import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import {postCurriculumService} from './CurriculumService';


const FlatButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

export default class CurriculumDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            messageTitle: '',
            titleIsValid: false,
            messageDescription: '',
            descriptionIsValid: false
        };
    }

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({
            open: false,
            messageTitle: '',
            messageDescription: '',
            titleIsValid: false,
            descriptionIsValid: false
        });
    };

    handleTitle = event => {
        const regex = /^.{4,50}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                messageTitle: '',
                title: event.target.value,
                titleIsValid: true,
            });
        } else {
            this.setState({
                messageTitle: 'Required a minimum length of 4 characters, maximum length of 50 characters',
                titleIsValid: false,
            });
        }
    };

    handleDescription = event => {
        const regex = /^.{10,500}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                messageDescription: '',
                description: event.target.value,
                descriptionIsValid: true,
            });
        } else {
            this.setState({
                messageDescription: 'Required a minimum length of 10 characters, maximum length of 500 characters',
                descriptionIsValid: false,
            });
        }
    };

    handleSubmit = () => {
        if(this.state.titleIsValid&this.state.descriptionIsValid){
            const data = {
                'title': this.state.title,
                'description': this.state.description
            };
            postCurriculumService(data).then(response => {
                this.props.getCurriculumsData();
                this.handleClose();
            });
        }
    };

    render() {
        const disable = !(this.state.titleIsValid&this.state.descriptionIsValid);
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
                    title={this.props.title}
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                >
                    <TextField
                        floatingLabelText="Name"
                        fullWidth={true}
                        onChange={this.handleTitle}
                        errorText={this.state.messageTitle} />
                    <TextField
                        defaultValue={this.props.description}
                        floatingLabelText="Description"
                        multiLine={true}
                        rows={2}
                        rowsMax={4}
                        fullWidth={true}
                        onChange={this.handleDescription}
                        errorText={this.state.messageDescription} />
                </Dialog>
            </div>
        );
    }
}
