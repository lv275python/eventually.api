import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import { postTopicService } from './TopicServices';


const FlatButtonStyle = {
    marginLeft: '93%',
    marginBottom: '20px',
};

export default class TopicDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            title: '',
            description: '',
        };
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

    handleSubmit = () => {
        const data = {
            'title': this.state.title,
            'description': this.state.description,
        };
        postTopicService(this.props.curriculumId, data).then(response => {
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
                        hintText="Title"
                        fullWidth={true}
                        onChange = {this.handleTitle} />
                    <TextField
                        hintText="Description"
                        multiLine={true}
                        rows={2}
                        rowsMax={4}
                        fullWidth={true}
                        onChange = {this.handleDescription} />
                </Dialog>
            </div>
        );
    }
}
