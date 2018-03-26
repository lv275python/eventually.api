import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import {putSuggestedTopicsItem} from './SuggestedTopicsService';


export default class SuggestedTopicsEdit extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            failNameMessage: '',
            failDescriptionMessage: '',
            nameIsValid: true,
            descriptionIsValid: true,
            open: false,
            name: this.props.name,
            description: this.props.description,
        };
    }

    /*update name*/
    handleName = event => {
        const regex = /^[\S\s].{4,64}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                failNameMessage: '',
                nameIsValid: true,
                name: event.target.value,
            });
        } else {
            this.setState({
                failNameMessage: 'Invalid name',
                nameIsValid: false
            });
        }
    };

    /*update description*/
    handleDescription = event => {
        const regex = /^[\S\s].{10,1024}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                failDescriptionMessage: '',
                descriptionIsValid: true,
                description: event.target.value
            });
        } else {
            this.setState({
                failDescriptionMessage: 'Invalid description',
                descriptionIsValid: false
            });
        }
    };

    /*save info from dialog*/
    handleSave = event => {
        const name = this.state.name;
        const description = this.state.description;
        const id = this.props.id;
        if(this.state.descriptionIsValid === true && this.state.nameIsValid === true){
            putSuggestedTopicsItem(id, name, description).then(response => {
                this.props.updateTopic(id, name, description);
                this.props.handleClose();
            });
        }
    };

    render() {
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.props.handleClose}
            />,
            <FlatButton
                label="Save"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleSave}
                disabled={this.state.descriptionIsValid === true & this.state.nameIsValid === true ? false : true}
            />,
        ];
        return (
            <Dialog
                title="Edit your Topic"
                actions={actions}
                modal={false}
                open={this.props.open}
                autoDetectWindowHeight={true}
                onRequestClose={this.props.handleClose}
            >
                <div>
                    <div>
                        <TextField
                            hintText="Name"
                            floatingLabelText="Enter name of topic that you suggest"
                            defaultValue={this.state.name}
                            fullWidth={true}
                            errorText={this.state.failNameMessage}
                            onChange={this.handleName}
                        />
                    </div>
                    <div>
                        <TextField
                            hintText="Description"
                            floatingLabelText="Enter description of topic you suggest"
                            defaultValue={this.state.description}
                            fullWidth={true}
                            errorText={this.state.failDescriptionMessage}
                            onChange={this.handleDescription}
                        />
                    </div>
                </div>
            </Dialog>
        );
    }
}
