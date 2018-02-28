import React from 'react';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import DatePicker from 'material-ui/DatePicker';
import {Card, CardHeader} from 'material-ui/Card';
import {putProfileService} from './ProfileService';
import {getImageUrl} from 'src/helper';
import {FileUpload} from 'src/containers';

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
            photo: this.props.profileData.photo,
            birthday: new Date(this.props.profileData.birthday)
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

    uploadImage = imageName => {
        this.setState({photo: imageName});
    }

    handleSave = () => {
        const firstName = this.state.firstName;
        const middleName = this.state.middleName;
        const lastName = this.state.lastName;
        const hobby = this.state.hobby;
        const photo = this.state.photo;
        const birthday = this.state.birthday.getFullYear() + '-' + (this.state.birthday.getMonth() + 1) + '-' + this.state.birthday.getDate();

        putProfileService(this.state.id, firstName, middleName, lastName, hobby, photo, birthday)
            .then(response => {
                this.props.onCloseClick();
            });
    };

    render() {
        return (
            <div style={styleMainDiv}>
                <Card style={styleCard}>
                    <CardHeader style = {styleHeader}
                        title="Edit profile"      
                        titleStyle={styleTitle}
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
                    </div>
                    <div style={styleContainer}>
                        <img src={this.state.photo && getImageUrl(this.state.photo)}
                            alt=""
                            style={imageStyle}
                        />
                    </div>
                    <FileUpload
                        updateImageNameInDb={this.uploadImage}
                    />
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
                </Card>
            </div>
        );
    }
}
