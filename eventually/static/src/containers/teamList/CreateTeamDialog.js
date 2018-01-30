import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import FileUpload from '../fileUpload/FileUpload';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import {teamServicePost} from './teamService';


const FlatButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

const CreateTeamDialogStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

export default class CreateTeamDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            name: '',
            description: '',
            image: '',
            owner: '1',
            members: [1],
        };
    }

    /*set description to state*/
    handleDescription = event => {
        this.setState({description: event.target.value});
    };

    /*set name to state*/
    handleName = event => {
        this.setState({name: event.target.value});
    };

    /*set uploaded image to state*/
    uploadImage = imageName => {
        this.setState({image: imageName});
    };

    /*open CreateTeamDialog*/
    handleOpen = () => {
        this.setState({ open: true });
    };

    /*close CreateTeamDialog*/
    handleClose = () => {
        this.setState({ open: false });
    };

    handleSubmit = () => {
        const data = {
            'name': this.state.name,
            'description': this.state.description,
            'image': this.state.image,
            'owner': this.state.owner,
            'members_id': this.state.members,
        };

        teamServicePost(data).then(response => {
            this.handleClose();
        });
    }

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
                        hintText="Name"
                        fullWidth={true}
                        defaultValue={this.props.title}
                        onChange={this.handleName}
                    />
                    <TextField
                        defaultValue={this.props.description}
                        hintText="Description"
                        multiLine={true}
                        rows={2}
                        rowsMax={4}
                        fullWidth={true}
                        onChange={this.handleDescription}
                    />
                    <FileUpload updateImageNameInDb={this.uploadImage}/>
                </Dialog>
            </div>
        );
    }
}
