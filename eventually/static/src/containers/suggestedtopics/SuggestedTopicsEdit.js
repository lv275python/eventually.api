import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import {putSuggestedTopicsItem} from './SuggestedTopicsService';



export default class SuggestedTopicsEdit extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: this.props.name,
            description: this.props.description,
            open: this.props.open
        };
    }

    /*update name*/
    handleName = event => {
        this.setState({name: event.target.value});
    };

    /*update description*/
    handleDescription = event => {
        this.setState({description: event.target.value});
    };

    /*save info from dialog*/
    handleSave = event => {
        const name = this.state.name;
        const description = this.state.description;
        const id = this.props.id;
        putSuggestedTopicsItem(id, name, description).then(response => {
            this.props.updateTopic(id, name, description);
            this.props.handleClose();
        });
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
                            onChange={this.handleName}
                        />
                    </div>
                    <div>
                        <TextField
                            hintText="Description"
                            floatingLabelText="Enter description of topic you suggest"
                            defaultValue={this.state.description}
                            fullWidth={true}
                            onChange={this.handleDescription}
                        />
                    </div>
                </div>
            </Dialog>
        );
    }
}