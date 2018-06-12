import React from 'react';
import Dialog from 'material-ui/Dialog';
import Dropzone from 'react-dropzone';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import Snackbar from 'material-ui/Snackbar';
import {s3Root} from 'src/helper';
import {sendFile, updateAssignmentStatus} from './FileUploadService';

const dialogStyle = {opacity: '0.98'};

const dropzoneStyle = { height : '100%',
    border : '1px dotted lightgrey',
    borderRadius: '5px',
    backgroundColor: '#fafdff',
    padding: '0px 10px 0px 10px',
    textAlign: 'center'};

const buttonStyle = {
    margin: '1% 15% -3%'};

export default class AssignmentUpload extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            fileName: 'Empty',
            open: false,
            fileData: '',
            fileKey: '',
        };
    }

    dialogOpen = () => {
        this.setState({open: true});
    };

    dialogClose = () => {
        this.setState({open: false});
    };

    dialogSubmit = () => {
        sendFile(this.state.fileData, 'doc').then(response => {
            this.setState({
                fileKey: response.data['file_key'],
                open: false,
            });
            updateAssignmentStatus(this.props.assignment_id, this.state.fileKey).then(response => {
                console.log(response);
            });
        })

    };

    updateFileName = (fileName) => {
        this.props.updateFileNameInDb(fileName);
    };


    onFileDrop = files => {
        let file = files[0];
        let fileData = new FormData();
        let fileType = file.type.slice(6);
        let fileSize = file.size;
        let fileName = file.name;

        // TODO add type and size validation

        fileData.append('file', file);
        this.setState({
            fileData: fileData,
            fileName: fileName,
        });

    };

    render() {
        const actions = [
            <FlatButton
                label='Cancel'
                primary={true}
                keyboardFocused={false}
                onClick={this.dialogClose}
            />,
            <FlatButton
                label='Upload'
                primary={true}
                keyboardFocused={false}
                onClick={this.dialogSubmit}
            />
        ];

        return (
            <div style={buttonStyle}>
                <RaisedButton
                    label='Upload Answer'
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
                        onDrop={this.onFileDrop}>
                        <p>Drop your document here</p>
                    </Dropzone>
                    <div>
                        <p>{this.state.fileName}</p>
                    </div>
                </Dialog>
            </div>
        );
    }
}
