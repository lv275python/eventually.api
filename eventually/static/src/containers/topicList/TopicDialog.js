import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import SelectField from 'material-ui/SelectField';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import { postTopicService } from './TopicServices';
import { CancelDialog } from 'src/containers';


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
            messageTitle: '',
            titleIsValid: false,
            messageDescription: '',
            descriptionIsValid: false,
            openCancelDialog: false
        };
    }

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({
            open: false,
            title: '',
            description: '',
            messageTitle: '',
            messageDescription: '',
            titleIsValid: false,
            descriptionIsValid: false
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
                messageTitle: 'Required a minimum length of 4 characters, maximum length of 255 characters',
                titleIsValid: false,
            });
        }
    };

    handleDescription = event => {
        const regex = /^.{10,1024}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                messageDescription: '',
                description: event.target.value,
                descriptionIsValid: true,
            });
        } else {
            this.setState({
                messageDescription: 'Required a minimum length of 10 characters, maximum length of 1024 characters',
                descriptionIsValid: false,
            });
        }
    };

    handleSubmit = () => {
        if(this.state.titleIsValid && this.state.descriptionIsValid){
            const data = {
                'title': this.state.title,
                'description': this.state.description,
            };
            postTopicService(this.props.curriculumId, data).then(response => {
                this.props.getTopicListData();
                this.handleClose();
            });
        }
    };

    handleCancelDialogClose = () => {
        this.setState({'openCancelDialog': false});
    };

    handleCancelCreateDialogClose = () => {
        this.handleCancelDialogClose();
        this.handleClose();
    };

    handleRequestClose = () => {
        if ((this.state.title != this.props.title) ||
            (this.state.description != this.props.description)) {
            this.setState({openCancelDialog: true});
        }
        else this.handleCancelCreateDialogClose();
    };

    render() {
        const disable = !(this.state.titleIsValid && this.state.descriptionIsValid);
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
                    mini={true}
                    onClick={this.handleOpen}
                    style={FlatButtonStyle}>
                    <ContentAdd />
                </FloatingActionButton>
                <Dialog
                    title={this.props.title}
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleRequestClose}
                >
                    <TextField
                        floatingLabelText="Title"
                        fullWidth={true}
                        onChange={this.handleTitle}
                        errorText={this.state.messageTitle} />
                    <TextField
                        floatingLabelText="Description"
                        multiLine={true}
                        rowsMax={4}
                        fullWidth={true}
                        onChange={this.handleDescription}
                        errorText={this.state.messageDescription} />
                </Dialog>
                {this.state.openCancelDialog &&
                    (<CancelDialog
                        openCancelDialog={this.state.openCancelDialog}
                        handleCancelMainDialogClose={this.handleCancelCreateDialogClose}
                        handleCancelDialogClose={this.handleCancelDialogClose}
                    />)
                }
            </div>
        );
    }
}
