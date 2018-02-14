import React from 'react';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import DatePicker from 'material-ui/DatePicker';
import {Card, CardHeader} from 'material-ui/Card';
import {putProfileService, getProfileService} from './ProfileService';
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
    }

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
                            onChange={this.props.onFirstNameChange}
                            hintText='First Name'
                            value={this.props.profileData.firstName}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Middle Name:"
                            onChange={this.props.onMiddleNameChange}
                            hintText='Middle Name'
                            value={this.props.profileData.middleName}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Last Name:"
                            onChange={this.props.onLastNameChange}
                            hintText='Last Name'
                            value={this.props.profileData.lastName}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Hobby:"
                            hintText='Hobby'
                            onChange={this.props.onHobbyChange}
                            fullWidth={true}
                            multiLine={true}
                            rowsMax={3}
                            value={this.props.profileData.hobby}
                        />
                        <DatePicker 
                            floatingLabelText="Birthday:"
                            hintText="Birthday"
                            mode="landscape"
                            openToYearSelection={true}
                            fullWidth={true}
                            onChange={this.props.onBirthdayChange}
                            value={this.props.profileData.birthday}
                        />
                    </div>
                    <div style={styleContainer}>
                        <img src={this.props.profileData.photo && getImageUrl(this.props.profileData.photo)}
                            alt=""
                            style={imageStyle}
                        />
                    </div>
                    <FileUpload
                        updateImageNameInDb={this.props.uploadImage}
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
                            onClick={this.props.onSaveClick}
                        />
                    </div>
                </Card>
            </div>
        );
    }
}
