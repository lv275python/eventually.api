import React from 'react';
import {getImageUrl} from 'src/helper';
import {getUserId} from 'src/helper';
import ProfileEdit from './ProfileEdit';
import {getProfileService} from './ProfileService';
import RaisedButton from 'material-ui/RaisedButton';


const styleMain = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    width: '100%',
    maxWidth: '640px',
    alignItems: 'center',
    boxShadow: '0px 0px 31px 2px rgba(0,0,0,0.53)',
    margin: '20px auto',
};

const styleLowerMain1 = {
    display: 'flex',
    justifyContent: 'center',
    width: '100%',
    margin: '10px 10px',
};

const styleLowerMain2 = {
    display: 'flex',
    justifyContent: 'flex-end',
    width: '85%',
    margin: '10px 10px',
};

const style_container = {
    width: '250px',
    height: '250px',
    fontSize: '10px',
    margin: '0 15px 0 0',
};

const styleInp = {
    fontSize: '25px',
    fontFamily: 'Roboto, sans-serif',
};

const styleSpan = {
    display: 'inline-block',
    fontSize: '15px',
    width: '117px',
};


export default class ProfileView extends React.Component {
    constructor(props) {
        super(props);
    }

    render(){
        const editBtn = this.props.isMyProfile ? 
            (<RaisedButton
                label="Edit"
                primary={true}
                keyboardFocused={true}
                onClick={this.props.onEditClick}
            />) : 
            null;
        return(
            <div style={styleMain}>
                <div style={styleLowerMain1}>
                    <div style={style_container}>
                        <img src={this.props.profileData.photo && getImageUrl(this.props.profileData.photo)}
                            alt=""
                            style={{maxHeight: '100%'}}
                        />
                    </div>
                    <div>
                        <p style={styleInp}><span style={styleSpan}>First Name:</span>{this.props.profileData.first_name}</p>
                        <p style={styleInp}><span style={styleSpan}>Middle Name:</span>{this.props.profileData.middle_name}</p> 
                        <p style={styleInp}><span style={styleSpan}>Last Name:</span>{this.props.profileData.last_name}</p> 
                        <p style={styleInp}><span style={styleSpan}>Hobby:</span>{this.props.profileData.hobby}</p>
                        <p style={styleInp}><span style={styleSpan}>Birthday:</span>{this.props.profileData.birthday.toDateString()}</p>
                    </div>
                </div>
                <div style={styleLowerMain2}>
                    {editBtn}
                </div>
            </div>
        );
    }
}
