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
import Dialog from 'material-ui/Dialog';
import Dropzone from 'react-dropzone';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import Snackbar from 'material-ui/Snackbar';
import {imageValidator} from './FileUploadHelper';
import {s3Root} from 'src/helper';

const dialogStyle = {opacity: '0.98'};

const dropzoneStyle = { height : '100%',
    border : '1px dotted lightgrey',
    borderRadius: '5px',
    backgroundColor: '#fafdff',
    padding: '0px 10px 0px 10px',
    textAlign: 'center'};

const buttonStyle = {
    margin: '1% 15% -3%'};

export default class FileUpload extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            imageName: '',
            imageSrc: s3Root + 'eventually-img/',
            open: false,
            snackbarOpen: false,
            snackbarMessage: '',
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
    };

    hideSnackbar = () => {
        this.setState({
            snackbarOpen: false,
        });
    };

    updateImageName = (imageName) => {
        this.props.updateImageNameInDb(imageName);
    };

    onImageDrop = files => {
        this.setState({'snackbarMessage': ''});
        let image = files[0];
        let imageData = new FormData();
        let imageType = image.type.slice(6);
        let imageSize = image.size;
        if (imageValidator(imageType, imageSize)) {
            imageData.append('image', image);
            this.props.fetchData(imageData, image['preview']);
            this.dialogClose();
        } else {
            this.setState({'snackbarMessage': 'Please choose another file'});
            this.showSnackbar();
        }
    };

    render() {
        const actions = [
            <FlatButton
                label='Cancel'
                primary={true}
                keyboardFocused={false}
                onClick={this.dialogClose}
            />
        ];

        return (
            <div style={buttonStyle}>
                <RaisedButton
                    label='Upload image'
                    primary={true}
                    onClick={this.dialogOpen}
                />
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
