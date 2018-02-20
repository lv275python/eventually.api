import React from 'react';
import {Link} from 'react-router';
import {getTeam} from './EventService';
import EventEdit from '../event/EventEdit';
import MapComponent from 'src/containers/event/Map';
import Paper from 'material-ui/Paper';


const STATUS_CHOICES = {
    0: 'draft',
    1: 'published',
    2: 'going',
    3: 'finished'
};

const styleTextDiv = {
    display: 'inline-block',
    width: '45%',
};

const stylePaper = {
    display: 'flex',
    margin: '1% 0%',
};

const styleInp = {
    fontSize: '15px',
    fontFamily: 'Roboto, sans-serif',
    fontWeight: 'normal',
};

const styleSpan = {
    margin_left: ' 0%',
    display: 'inline-block',
    fontSize: '15px',
    width: '35%',
    fontWeight: 'bold',

};

const styleMain = {
    width: '100%',
    margin: '1% 4%',
    paddingLeft: '10%',
    paddingRight: '0%',
    paddingBottom: '1%',
};

const styleMap = {
    display: 'inline-block',
    width: '50%',
};

class Event extends React.Component {

    constructor(props) {

        super(props);
        this.state = {
            team: this.props.team,
            owner: this.props.owner,
            name: this.props.name,
            description: this.props.description,
            startAt: this.props.startAt,
            createdAt: this.props.createdAt,
            updatedAt: this.props.updatedAt,
            duration: this.props.duration,
            longitude: this.props.longitude,
            latitude: this.props.latitude,
            budget: this.props.budget,
            status: this.props.status,
            id: this.props.id,
            isMarkerShown: false,
        };
    }

    componentWillMount() {
        let durationString = '';
        durationString += Math.trunc(this.state.duration / (3600 * 24)) + 'd ';
        durationString += Math.trunc((this.state.duration % (3600 * 24)) / 3600) + 'h ';
        durationString += Math.trunc((this.state.duration % 3600) / 60) + 'm';
        this.setState({durationString: durationString});
    }


    render() {
        return (
            <div>
                <Paper style={stylePaper} zDepth={4}>
                    <div style={styleMain}>
                        <div style={styleTextDiv}>
                            <p style={styleInp}><span style={styleSpan}>Name :</span>{this.state.name}</p>
                            <p style={styleInp}><span style={styleSpan}>Description :</span>{this.state.description}</p>
                            <p style={styleInp}><span style={styleSpan}>Owner :</span>{this.state.owner}</p>
                            <p style={styleInp}><span
                                style={styleSpan}>Start at :</span>{(new Date(this.state.startAt * 1000)).toDateString()}
                            </p>
                            <p style={styleInp}><span
                                style={styleSpan}>Created at :</span>{(new Date(this.state.createdAt * 1000)).toDateString()}
                            </p>
                            <p style={styleInp}><span
                                style={styleSpan}>Updated at :</span>{(new Date(this.state.updatedAt * 1000)).toDateString()}
                            </p>
                            <p style={styleInp}><span style={styleSpan}>Duration :</span>{this.state.durationString}</p>
                            <p style={styleInp}><span style={styleSpan}>Budget :</span>{this.state.budget}</p>
                            <p style={styleInp}><span
                                style={styleSpan}>Status :</span>{STATUS_CHOICES [this.state.status]}
                            </p>
                            {this.state.id && (
                                <EventEdit
                                    key={this.props.id.toString()}
                                    team={this.props.team}
                                    owner={this.props.owner}
                                    name={this.props.name}
                                    description={this.props.description}
                                    startAt={this.props.startAt}
                                    createdAt={this.props.createdAt}
                                    updatedAt={this.props.updatedAt}
                                    duration={this.props.duration}
                                    longitude={this.props.longitude}
                                    latitude={this.props.latitude}
                                    budget={this.props.budget}
                                    status={this.props.status}
                                    id={this.props.id}
                                />
                            )}
                        </div>
                        <div style={styleMap}>
                            <MapComponent
                                longitude={this.props.longitude}
                                latitude={this.props.latitude}
                                name ={this.props.name}
                            />
                        </div>
                    </div>
                </Paper>
            </div>

        );
    }
}

export default Event;
