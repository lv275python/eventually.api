import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import TextField from 'material-ui/TextField';
import ContentAdd from 'material-ui/svg-icons/content/add';
import {postSuggestedTopicsItem} from './SuggestedTopicsService';


const FlatButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};


export default class SuggestedTopicCreate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            validationField: {
                failNameMessage: '',
                failDescriptionMessage: ''
            },
            open: false,
            name: '',
            description: '',
        };
    }

    handleChangeName = event => {
        const regex = /^[\S\s].{4,64}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                failNameMessage: '',
                name: event.target.value,
            });
        } else {
            this.setState({
                failNameMessage: 'Invalid name',
            });
        }
    };

    handleChangeDescription = event => {
        const regex = /^[\S\s].{10,1024}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                failDescriptionMessage: '',
                description: event.target.value
            });
        } else {
            this.setState({
                failDescriptionMessage: 'Invalid description'
            });
        }
    };

    handleSubmit = event => {
        const data = {
            'name': this.state.name,
            'description': this.state.description
        };
        postSuggestedTopicsItem(data).then(response => {
                this.props.getSuggestedTopicsItem();
                this.handleClose();
            });
    };

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({ open: false });
        this.setState({
            name: '',
            description: ''
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
                disabled={this.state.name.length >= 4 & this.state.description.length >= 10 ? false : true}
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
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                    style={{zIndex: 800}}>
                    <TextField
                        hintText="minimum 4 characters"
                        floatingLabelText="Enter name of topic that you suggest"
                        defaultValue={this.state.name}
                        fullWidth={true}
                        errorText={this.state.failNameMessage}
                        onChange={this.handleChangeName}/>
                    <TextField
                        hintText="minimum 10 characters"
                        floatingLabelText="Enter description of topic you suggest"
                        defaultValue={this.state.description}
                        fullWidth={true}
                        multiLine={true}
                        rowsMax={4}
                        errorText={this.state.failDescriptionMessage}
                        onChange={this.handleChangeDescription}/>
                </Dialog>
            </div>
        );
    }
}

