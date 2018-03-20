import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import {FileUpload, CancelDialog} from 'src/containers';
import {teamServicePut} from './teamService';


export default class EditTeamDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: this.props.name,
            description: this.props.description,
            image: this.props.image,
            openMore:false,
            openCancelDialog: false
        };
    }
    /*upload image to state*/
    uploadImage = imageName => {
        this.setState({image: imageName});
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
        const new_image = this.state.image;
        const id = this.props.id;
        teamServicePut(id, name, description, new_image).then(response => {
            this.props.updateItem(id, name, description, new_image);
            this.props.handleClose();
        });
    };

    handleCancelDialogClose = () => {
        this.setState({'openCancelDialog': false});
    };

    handleCancelEditDialogClose = () => {
        this.setState ({
            name: this.props.name,
            description: this.props.description,
            image:this.props.image,
        });
        this.handleCancelDialogClose();
        this.props.handleClose();
    };

    handleRequestClose = () => {
        if ((this.state.name != this.props.name) ||
            (this.state.description != this.props.description) ||
            (this.state.image != this.props.image)) {
            this.setState({openCancelDialog: true});
        }
        else this.props.handleClose();
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
            <div>
                <Dialog
                    title="Edit Your Team"
                    actions={actions}
                    modal={false}
                    open={this.props.open}
                    autoDetectWindowHeight={true}
                    onRequestClose={this.handleRequestClose}
                >
                    <div>
                        <div>
                            <TextField
                                hintText="Name of Team"
                                floatingLabelText="Enter name of your team"
                                defaultValue={this.state.name}
                                fullWidth={true}
                                onChange={this.handleName}
                            />
                        </div>
                        <div>
                            <TextField
                                hintText="Description"
                                floatingLabelText="Enter description of your team"
                                defaultValue={this.state.description}
                                fullWidth={true}
                                onChange={this.handleDescription}
                            />
                        </div>
                        <FileUpload updateImageNameInDb={this.uploadImage}/>
                    </div>
                </Dialog>
                {this.state.openCancelDialog &&
                    (<CancelDialog
                        openCancelDialog={this.state.openCancelDialog}
                        handleCancelMainDialogClose={this.handleCancelEditDialogClose}
                        handleCancelDialogClose={this.handleCancelDialogClose}
                    />)
                }
            </div>
        );
    }
}
