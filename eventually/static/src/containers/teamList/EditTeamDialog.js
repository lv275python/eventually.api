import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import LinearProgress from 'material-ui/LinearProgress';
import TextField from 'material-ui/TextField';
import {FileUpload, CancelDialog, sendFile} from 'src/containers';
import {getImageUrl} from 'src/helper';
import {deleteFile} from '../fileUpload/FileUploadService';
import {teamServicePut} from './teamService';

const styleContainer = {
    width: '150px',
    height: '150px',
    margin:'0% 15%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
};

const imageStyle = {
    maxWidth: '100%',
    maxHeight: '100%',
};

export default class EditTeamDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: this.props.name,
            description: this.props.description,
            imageName: this.props.image,
            openMore:false,
            imageData: {},
            imageUrl: getImageUrl(this.props.image),
            linearProgressVisibility: 'hidden',
            openCancelDialog: false
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

    showLinearProgress = () => {
        this.setState({linearProgressVisibility: 'visible'});
    }

    hideLinearProgress = () => {
        this.setState({linearProgressVisibility: 'hidden'});
    }

    /*save info from dialog*/
    handleSave = event => {
        this.showLinearProgress();

        const oldImageName = this.state.imageName;

        sendFile(this.state.imageData).then(response => {
            if (response.status == 200) {
                this.setState({
                    imageName: response.data['image_key']
                });

                this.hideLinearProgress();

                teamServicePut(
                    this.props.id,
                    this.state.name,
                    this.state.description,
                    response.data['image_key']
                ).then(response => {
                    this.props.updateItem(
                        this.props.id,
                        this.state.name,
                        this.state.description,
                        this.state.imageName
                    );
                    this.props.handleClose();
                });

                deleteFile(oldImageName);
            }
        }).catch(error => {
            this.hideLinearProgress();
        });
    };

    fetchData = (imageData, imageUrl) => {
        this.setState({
            imageData: imageData,
            imageUrl: imageUrl
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
        const linearProgressStyle = {'visibility': this.state.linearProgressVisibility};

        const linearProgressWrapperStyle = {position: 'relative', top: 5};

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
            <div style={linearProgressWrapperStyle}>
                <LinearProgress mode='indeterminate' style = {linearProgressStyle}/>
            </div>
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
                    </div>
                    <div style={styleContainer}>
                        <img src={this.state.imageUrl}
                            alt=""
                            style={imageStyle}
                        />
                    </div>
                    <FileUpload
                        fetchData={this.fetchData}
                    />
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
