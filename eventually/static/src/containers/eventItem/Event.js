import React from 'react';
import {Link} from 'react-router';
import RaisedButton from 'material-ui/RaisedButton';
import {getEvent, getOwner, getTeam} from './EventItemService';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import EventEdit from '../event/EventEdit';
import EventTaskList from '../eventTaskList/EventTaskList';
//
const STATUS_CHOICES = {
    0: 'draft',
    1: 'published',
    2: 'going',
    3: 'finished'
};

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

const buttonStyle = {
    border: '2px solid #B3E5FC',
    margin: '1%',
    width: '10%',
    display: 'inline-block',
};

class Event extends React.Component {

    constructor(props) {

        super(props);
        // this.state = {
        //     team: '',
        //     owner_id: '1',
        //     name: '',
        //     description: '',
        //     start_at: '',
        //     created_at: '',
        //     updated_at: '',
        //     duration: '',
        //     longitude: '',
        //     latitude: '',
        //     budget: '',
        //     status: '',
        //     id: '',
        //     team_id:'',
        //     owner:'',
        // };
    }


    componentWillMount() {
        this.getDataEvent();
        this.getDataOwner();
        this.getDataTeam();
    }

    getDataEvent=()=>{
        getEvent(this.props.match.params.eventId).then(response => {
            this.setState({
                'team_id': response.data['team'],
                'owner_id': response.data['owner'],
                name: response.data['name'],
                description: response.data['description'],
                start_at: response.data['start_at'],
                created_at: response.data['created_at'],
                updated_at: response.data['updated_at'],
                duration: response.data['duration'],
                longitude: response.data['longitude'],
                latitude: response.data['latitude'],
                budget: response.data['budget'],
                status: response.data['status'],
                id:response.data['id']

            });
        });
    }
    getDataOwner=()=> {
        getOwner(this.state.owner_id).then(response => {
            const name = (response.data['first_name'] + ' ' + response.data['last_name']);
            this.setState({
                owner: name
            });
        });
    }

    getDataTeam=()=>{
        getTeam(this.state.team_id).then(response => {
            const name = (response.data['name']);
            this.setState({
                team: name
            });
        });
    }

    render() {

        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleClose}
            />,
        ];

        return (
            <div >
                <RaisedButton label="Details" onClick={this.handleOpen} style={buttonStyle}/>
                <div style={styleLowerMain1}>
                    <div>
                        <p style={styleInp}><span style={styleSpan}>Name :</span>{this.state.name}</p>
                        <p style={styleInp}><span style={styleSpan}>Description :</span>{this.state.description}</p>
                        <p style={styleInp}><span style={styleSpan}>Owner :</span>{this.state.owner}</p>
                        <p style={styleInp}><span style={styleSpan}>Start at :</span>{(new Date(this.state.start_at*1000)).toDateString()}</p>
                        <p style={styleInp}><span style={styleSpan}>Created at :</span>{(new Date(this.state.created_at*1000)).toDateString()}</p>
                        <p style={styleInp}><span style={styleSpan}>Updated at :</span>{(new Date(this.state.updated_at*1000)).toDateString()}</p>
                        <p style={styleInp}><span style={styleSpan}>Duration :</span>{Math.floor(this.state.duration / 3600) + ':' + Math.floor(this.state.duration % 3600 / 60) }</p>
                        <p style={styleInp}><span style={styleSpan}>Budget :</span>{this.state.budget}</p>
                        <p style={styleInp}><span style={styleSpan}>Status :</span>{STATUS_CHOICES [this.state.status]}</p>
                    </div>
                </div>
                {/*<div style={styleLowerMain2}>*/}
                    {/*<EventEdit*/}
                        {/*key={this.state.id.toString()}*/}
                        {/*team={this.state.team_id}*/}
                        {/*owner={this.state.owner}*/}
                        {/*name={this.state.name}*/}
                        {/*description={this.state.description}*/}
                        {/*start_at={this.state.start_at}*/}
                        {/*created_at={this.state.created_at}*/}
                        {/*updated_at={this.state.updated_at}*/}
                        {/*duration={this.state.duration}*/}
                        {/*longitude={this.state.longitude}*/}
                        {/*latitude={this.state.latitude}*/}
                        {/*budget={this.state.budget}*/}
                        {/*status={this.state.status}*/}
                        {/*id={this.state.id}*/}
                    {/*/>*/}
                {/*</div>*/}
                {/*<EventTaskList*/}
                    {/*eventId={this.state.id}*/}
                    {/*team={this.state.team_id}*/}
                    {/*name={this.state.name}*/}
                    {/*description={this.state.description}/>*/}

            </div>
        );
    }
}

export default Event;
