import React from 'react';
import {putProfileService, getProfileService} from './ProfileService.js';
import {getImageUrl} from '../../helper';
import FileUpload from '../fileUpload/FileUpload';

import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import DatePicker from 'material-ui/DatePicker';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';


const style_card = {
    display: 'flex',
    justifyContent: 'center',
};

const style_name = {
    margin: '10px 100px 0 100px',
    height: '400px',
    width: '400px',
};

const style_main_div = {
    display: 'flex',
    justifyContent: 'center',
};
const style_title = {      
    fontSize: '35px',     
};

const style_header = {        
    display: 'flex',      
    alignItems: 'center',     
    justifyContent: 'center',     
};

const style_buttons = {        
    display: 'flex',      
    alignItems: 'center',     
    justifyContent: 'space-between',    
    margin: '20px 80px 40px 100px' , 
    width: '80%',
};

const style_container = {
    width: '150px',
    height: '150px',
    margin:'0px 100px',
};

export default class ProfileEdit extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: '',
            first_name: '',
            middle_name: '', 
            last_name: '',
            hobby: '',
            photo: '',
            birthday: '1970.1.1'
        };
    }
        
    componentWillMount(){
        this.getProfile();
    }
    getProfile = () => {
        getProfileService().then(response => {

            this.setState({'id': response.data['user'],
                first_name: response.data['first_name'],
                middle_name: response.data['middle_name'], 
                last_name: response.data['last_name'],
                hobby: response.data['hobby'],
                photo: response.data['photo'],
                birthday: new Date(response.data['birthday'])});
        }, error => {
            console.log(error);    
        });                  
    };    

    handleFirstName = event => {
        this.setState({first_name: event.target.value});
    };

    handleMiddleName = event => {
        this.setState({middle_name: event.target.value});
    };

    handleLastName = event => {
        this.setState({last_name: event.target.value});
    };

    handleHobby = event => {
        this.setState({hobby: event.target.value});
    };

    handleBirthday = (event, date) => {
        this.setState({birthday: date});
    };
    
    handleSave = () => {
        const first_name = this.state.first_name;
        const middle_name = this.state.middle_name;
        const last_name = this.state.last_name;
        const hobby = this.state.hobby;
        const photo = this.state.photo;
        const birthday = this.state.birthday.getTime()/1000;
        

        putProfileService(this.state.id, first_name, middle_name, last_name, hobby, photo, birthday)
            .then(response => {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    uploadImage = imageName => {
        this.setState({photo: imageName});
    }
    
    render() {
        return (
            <div style={style_main_div}>
                <Card style={style_card}>
                    <CardHeader style = {style_header}      
                        title="Edit profile"      
                        titleStyle={style_title}        
                    />
                    <div style={style_name}>
                        <TextField
                            floatingLabelText="First Name:"
                            onChange={this.handleFirstName}
                            hintText='First Name'
                            value={this.state.first_name}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Middle Name:"
                            onChange={this.handleMiddleName}
                            hintText='Middle Name'
                            value={this.state.middle_name}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Last Name:"
                            onChange={this.handleLastName}
                            hintText='Last Name'
                            value={this.state.last_name}
                            fullWidth={true}

                        />
                        <TextField
                            floatingLabelText="Hobby:"
                            hintText='Hobby'
                            onChange={this.handleHobby}
                            fullWidth={true}
                            multiLine={true}
                            rowsMax={3}
                            value={this.state.hobby}
                        />
                        <DatePicker 
                            floatingLabelText="Birthday:"
                            hintText="Birthday"
                            Dialog mode="landscape" 
                            openToYearSelection={true}
                            fullWidth={true}
                            onChange={this.handleBirthday}
                            value={new Date(this.state.birthday)}
                        />
                    </div>
                    <div style={style_container}>
                        <img src={getImageUrl(this.state.photo)}
                            alt=""
                            style={{maxHeight: '100%'}}
                        />
                    </div>
                        
                    <div style={style_buttons}>
                        <FileUpload updateImageNameInDb={this.uploadImage}/>
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
