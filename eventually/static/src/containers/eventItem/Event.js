import React from 'react';
import {Link} from 'react-router';
import RaisedButton from 'material-ui/RaisedButton';
import {getOwner, getTeam} from './EventItemService';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import EventEdit from '../event/EventEdit';
import EventTaskList from '../eventTaskList/EventTaskList';

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
        this.state = {
            open: false,
            team: this.props.team,
            owner: this.props.owner,
            name: this.props.name,
            description: this.props.description,
            start_at: this.props.start_at,
            created_at: this.props.created_at,
            updated_at: this.props.updated_at,
            duration: this.props.duration,
            longitude: this.props.longitude,
            latitude: this.props.latitude,
            budget: this.props.budget,
            status: this.props.status,
            id: this.props.id,
        };
    }

    handleOpen = () => {
        this.setState({open: true});
    };

    handleClose = () => {
        this.setState({open: false});
    };

    componentWillMount() {

        getOwner(this.state.owner).then(response => {
            const name = (response.data['first_name'] + ' ' + response.data['last_name']);
            this.setState({
                owner: name
            });
        });

        getTeam(this.state.team).then(response => {
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
                
                <Dialog
                    title="Dialog With Actions"
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                    autoScrollBodyContent={true}
                >
                    <div style={styleLowerMain1}>
                        <div>
                            <p style={styleInp}><span style={styleSpan}>Name :</span>{this.state.name}</p>
                            <p style={styleInp}><span style={styleSpan}>Description :</span>{this.state.description}</p>
                            <p style={styleInp}><span style={styleSpan}>Owner :</span>{this.state.owner}</p>
                            <p style={styleInp}><span style={styleSpan}>Start at :</span>{(new Date(this.state.start_at)).toDateString()}</p>
                            <p style={styleInp}><span style={styleSpan}>Created at :</span>{(new Date(this.state.created_at)).toDateString()}</p>
                            <p style={styleInp}><span style={styleSpan}>Updated at :</span>{(new Date(this.state.updated_at)).toDateString()}</p>
                            <p style={styleInp}><span style={styleSpan}>Duration :</span>{Math.floor(this.state.duration / 3600) + ':' + Math.floor(this.state.duration % 3600 / 60) }</p>
                            <p style={styleInp}><span style={styleSpan}>Budget :</span>{this.state.budget}</p>
                            <p style={styleInp}><span style={styleSpan}>Status :</span>{STATUS_CHOICES [this.state.status]}</p>
                        </div>
                    </div>
                    <div style={styleLowerMain2}>
                        <EventEdit 
                            key={this.props.id.toString()}
                            team={this.props.team}
                            owner={this.props.owner}
                            name={this.props.name}
                            description={this.props.description}
                            start_at={this.props.start_at}
                            created_at={this.props.created_at}
                            updated_at={this.props.updated_at}
                            duration={this.props.duration}
                            longitude={this.props.longitude}
                            latitude={this.props.latitude}
                            budget={this.props.budget}
                            status={this.props.status}
                            id={this.props.id}
                        />
                    </div>
                    <EventTaskList eventId={this.props.id}
                                   team={this.props.team}
                                   name={this.props.name}
                                   description={this.props.description}/>
                </Dialog>
            </div>
        );
    }
}

export default Event;
