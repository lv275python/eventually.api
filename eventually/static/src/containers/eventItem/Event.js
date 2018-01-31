import React from 'react';
import {Link} from 'react-router';
import RaisedButton from 'material-ui/RaisedButton';
import {getOwner, getTeam} from './EventItemService';
const STATUS_CHOICES = {
    0: 'draft',
    1: 'published',
    2: 'going',
    3: 'finished'
};
const myDate = new Date();
myDate.setMilliseconds(1800);
console.log(myDate);
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

const styleInp = {
    fontSize: '25px',
    fontFamily: 'Roboto, sans-serif',
};

const styleSpan = {
    display: 'inline-block',
    fontSize: '15px',
    width: '117px',
};
const styleLowerMain2 = {
    display: 'flex',
    justifyContent: 'flex-end',
    width: '85%',
    margin: '10px 10px',
};

class Event extends React.Component {

    constructor(props) {

        super(props);
        this.state = {
            event: props.location.state.event,
            owner: '',
            team: ''
        };
    }

    componentWillMount() {

        getOwner(this.state.event.owner).then(response => {
            const name = (response.data['first_name'] + ' ' + response.data['last_name']);
            this.setState({
                owner: name
            });
        });

        getTeam(this.state.event.team).then(response => {
            const name = (response.data['name']);
            this.setState({
                team: name
            });
        });

    }

    render() {
        return (
            <div style={styleMain}>
                <div style={styleLowerMain1}>

                    <div>
                        <p style={styleInp}><span style={styleSpan}>Name :</span>{this.state.event.name}</p>
                        <p style={styleInp}><span style={styleSpan}>Description :</span>{this.state.event.description}</p>
                        <p style={styleInp}><span style={styleSpan}>Owner :</span>{this.state.owner}</p>
                        <p style={styleInp}><span style={styleSpan}>Start at :</span>{(new Date(this.state.event.start_at)).toDateString()}</p>
                        <p style={styleInp}><span style={styleSpan}>Created at :</span>{(new Date(this.state.event.created_at)).toDateString()}</p>
                        <p style={styleInp}><span style={styleSpan}>Updated at :</span>{(new Date(this.state.event.updated_at)).toDateString()}</p>
                        <p style={styleInp}><span style={styleSpan}>Duration :</span>{Math.floor(this.state.event.duration / 3600) + ':' + Math.floor(this.state.event.duration % 3600 / 60) }</p>
                        <p style={styleInp}><span style={styleSpan}>Budget :</span>{this.state.event.budget}</p>
                        <p style={styleInp}><span style={styleSpan}>Status :</span>{STATUS_CHOICES [this.state.event.status]}</p>
                    </div>
                </div>
                <div style={styleLowerMain2}>
                    <RaisedButton
                        label="Edit"
                        primary={true}
                        keyboardFocused={true}

                    />
                </div>
            </div>
        );
    }
}

export default Event;
