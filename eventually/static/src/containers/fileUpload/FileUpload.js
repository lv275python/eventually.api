/*  Image Upload button component
    
    Accepts GIF, PNG, JPG and BMP images only.
    Size should be less than 8Mb.

    Timeout for the upload is 30 sec.

    You can provide your custom function to upload image to your DB table
    by passing the function as the "updateImageNameInDb" property.
    E.G.: 
        const uploadImage = (imageName) => {
            //function to upload image to the db.
        };
        ...
        <FileUpload updateImageNameInDb={uploadImage}/>
 */

import React from 'react';
import Dropzone from 'react-dropzone';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import LinearProgress from 'material-ui/LinearProgress';
import Snackbar from 'material-ui/Snackbar';
import {imageValidator} from './FileUploadHelper';
import {sendFile} from './FileUploadService';
import {s3Root} from 'src/helper';

const dialogStyle = {opacity: '0.98'};

const dropzoneStyle = { height : '100%', 
    border : '1px dotted lightgrey',
    borderRadius: '5px',
    backgroundColor: '#fafdff',
    padding: '0px 10px 0px 10px',
    textAlign: 'center'};

const buttonStyle = {
    margin: '1% 15% -5%' };

export default class FileUpload extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            imageName: '',
            imageSrc: s3Root,
            open: false,
            snackbarOpen: false,
            snackbarMessage: '',
            linearProgressVisibility: 'hidden'
        };
    }

    dialogOpen = () => {
        this.setState({open: true});
    };

    dialogClose = () => {
        this.setState({open: false});
    };

    showSnackbar = () => {
        this.setState({
            snackbarOpen: true,
        });
    }

    hideSnackbar = () => {
        this.setState({
            snackbarOpen: false,
        });
    }

    showLinearProgress = () => {
        this.setState({linearProgressVisibility: 'visible'});
    }

    hideLinearProgress = () => {
        this.setState({linearProgressVisibility: 'hidden'});
    }

    updateImageName = (imageName) => {
        this.props.updateImageNameInDb(imageName);
    }

    onImageDrop = files => {
        this.setState({'snackbarMessage': ''});
        let image = files[0];
        let data = new FormData();
        let imageType = image.type.slice(6);
        let imageSize = image.size;
        if (imageValidator(imageType, imageSize)) {
            this.showLinearProgress();
            data.append('image', image);
            data.append('image', image);
            sendFile(data).then( (response)=>{
                if (response.status == 200) {
                    this.setState({
                        'imageName': response.data['image_key'],
                        'imageSrc': this.state.imageSrc.slice(0,53)+response.data['image_key'],
                        'snackbarMessage': 'Image uploaded'});
                    this.hideLinearProgress();
                    this.dialogClose();
                    this.showSnackbar();
                    this.updateImageName(response.data['image_key']);
                }
            }).catch( (error) => {
                this.setState({'snackbarMessage': 'Upload timed out'});
                this.hideLinearProgress();
                this.dialogClose();
                this.showSnackbar();
            });
        }
        else {
            this.hideLinearProgress();
            this.setState({'snackbarMessage': 'Please choose another file'});
            this.showSnackbar();
        }
    }

    render() {
        const actions = [
            <FlatButton
                label='Cancel'
                primary={true}
                keyboardFocused={false}
                onClick={this.dialogClose}
            />
        ];

        const linearProgressStyle = {'visibility': this.state.linearProgressVisibility};

        const linearProgressWrapperStyle = {position: 'relative', top:'20px'};

        return (
            <div style={buttonStyle}>
                <RaisedButton label='Upload image' primary={true} onClick={this.dialogOpen}/>
                <Dialog
                    title='File Upload'
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    style={dialogStyle}
                    onRequestClose={this.dialogClose}>
                    <Dropzone
                        multiple={false}
                        style={dropzoneStyle}
                        onDrop={this.onImageDrop}>
                        <p>Drop an image here or click to upload the file.<br/>
                        The file must be of GIF, PNG, JPG or BMP type.<br/>
                        Maximum file size: 8 Mb</p>
                    </Dropzone>
                    <div style={linearProgressWrapperStyle}>
                        <LinearProgress mode='indeterminate' style = {linearProgressStyle}/>
                    </div>
                </Dialog>
                <Snackbar
                    style={{textAlign:'center'}}
                    open={this.state.snackbarOpen}
                    message={this.state.snackbarMessage}
                    autoHideDuration={5000}
                    onRequestClose={this.hideSnackbar}
                />
            </div>
        );
    }
}
