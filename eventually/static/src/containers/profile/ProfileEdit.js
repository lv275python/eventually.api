import React from 'react';
import {Card, CardHeader} from 'material-ui/Card';
import DatePicker from 'material-ui/DatePicker';
import LinearProgress from 'material-ui/LinearProgress';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import {FileUpload} from 'src/containers';
import {getImageUrl} from 'src/helper';
import {putProfileService, putProfileServicePhoto} from './ProfileService';
import {sendFile} from '../fileUpload/FileUploadService';
import ChangePassword from './ChangePassword';

const styleCard = {
    display: 'flex',
    justifyContent: 'center',
};

const styleName = {
    margin: '10px 100px 0 100px',
    height: '400px',
    width: '400px',
};

const styleMainDiv = {
    display: 'flex',
    justifyContent: 'center',
};
const styleTitle = {
    fontSize: '35px',
};

const styleHeader = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
};

const styleButtons = {
    display: 'flex',
    alignItems: 'flex-end',
    justifyContent: 'space-around',
    margin: '20px 20px 40px 350px' ,
    width: '40%',
};

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


export default class ProfileEdit extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: this.props.profileData.id,
            firstName: this.props.profileData.firstName,
            middleName: this.props.profileData.middleName,
            lastName: this.props.profileData.lastName,
            hobby: this.props.profileData.hobby,
            imageName: this.props.profileData.photo,
            birthday: new Date(this.props.profileData.birthday),
            imageData: {},
            imageUrl: this.props.profileData.photo && getImageUrl(this.props.profileData.photo),
            linearProgressVisibility: 'hidden'
        };
    }

    handleFirstNameChange = event => {
        this.setState({
            firstName: event.target.value
        });
    };

    handleMiddleNameChange = event => {
        this.setState({
            middleName: event.target.value
        });
    };

    handleLastNameChange = event => {
        this.setState({
            lastName: event.target.value
        });
    };

    handleHobbyChange = event => {
        this.setState({
            hobby: event.target.value
        });
    };

    handleBirthdayChange = (event, date) => {
        this.setState({
            birthday: date
        });
    };

    getBirthday = () => {
        return this.state.birthday.getFullYear() + '-' +
               (this.state.birthday.getMonth() + 1) + '-' +
               this.state.birthday.getDate();
    };

    showLinearProgress = () => {
        this.setState({linearProgressVisibility: 'visible'});
    };

    hideLinearProgress = () => {
        this.setState({linearProgressVisibility: 'hidden'});
    };

    handleSave = () => {
        this.showLinearProgress();

        putProfileService(
            this.state.id,
            this.state.firstName,
            this.state.middleName,
            this.state.lastName,
            this.state.hobby,
            this.getBirthday()
        ).then(() => {
            this.props.onCloseClick();
        });
    };

    handleSavePhoto = () => {
        this.showLinearProgress();

        sendFile(this.state.imageData, 'img').then(response => {
            this.setState({
                imageName: response.data['image_key']
            });
        }).then( () => {
            putProfileServicePhoto(this.state.id,
                this.state.imageName
            ).then(response => {
                this.props.onCloseClick();
            });
            this.hideLinearProgress();
        }).catch(error => {
            this.hideLinearProgress();
        });
    };

    fetchData = (imageData, imageUrl) => {
        this.setState({
            imageData: imageData,
            imageUrl: imageUrl
        }, () => { this.handleSavePhoto(); });
    };

    render() {
        const linearProgressStyle = {'visibility': this.state.linearProgressVisibility};

        const linearProgressWrapperStyle = {position: 'relative', bottom: 30};

        return (
            <div style={styleMainDiv}>
                <Card style={styleCard}>
                    <CardHeader style = {styleHeader}
                        title="Edit profile"
                        titleStyle={styleTitle}
                    />
                    <div style={styleContainer}>
                        <img src={this.state.imageUrl}
                            alt=""
                            style={imageStyle}
                        />
                    </div>
                    <FileUpload
                        fetchData={this.fetchData}
                        handleSavePhoto={this.handleSavePhoto}
                    />
                    <div style={styleName}>
                        <TextField
                            floatingLabelText="First Name:"
                            onChange={this.handleFirstNameChange}
                            hintText='First Name'
                            value={this.state.firstName}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Middle Name:"
                            onChange={this.handleMiddleNameChange}
                            hintText='Middle Name'
                            value={this.state.middleName}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Last Name:"
                            onChange={this.handleLastNameChange}
                            hintText='Last Name'
                            value={this.state.lastName}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Hobby:"
                            hintText='Hobby'
                            onChange={this.handleHobbyChange}
                            fullWidth={true}
                            multiLine={true}
                            rowsMax={3}
                            value={this.state.hobby}
                        />
                        <DatePicker
                            floatingLabelText="Birthday:"
                            hintText="Birthday"
                            mode="landscape"
                            openToYearSelection={true}
                            fullWidth={true}
                            onChange={this.handleBirthdayChange}
                            value={this.state.birthday}
                        />
                        <ChangePassword />
                    </div>
                    <div style={styleButtons}>
                        <RaisedButton
                            label="Cancel"
                            secondary={true}
                            keyboardFocused={true}
                            onClick={this.props.onCloseClick}
                        />
                        <RaisedButton
                            label="Save"
                            primary={true}
                            keyboardFocused={true}
                            onClick={this.handleSave}
                        />
                    </div>
                    <div style={linearProgressWrapperStyle}>
                        <LinearProgress mode='indeterminate' style = {linearProgressStyle}/>
                    </div>
                </Card>
            </div>
        );
    }
}
