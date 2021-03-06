import React from 'react';
import Snackbar from 'material-ui/Snackbar';
import isEqual from 'lodash/isEqual';
import { eventTasksServiceGet, eventServiceGet, eventTaskServicePut, taskGetTeamService, getOwner } from './EventService';
import Event from './Event';
import EventTaskList from './EventTaskList';


const containerStyle = {
    width: '99%',
    margin: '0 auto',
};

export default class EventDetails extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.match.params.eventId,
            teamId: null,
            owner: this.props.owner,
            eventName: '',
            eventDescription: '',
            members: [],
        };
    }

    componentWillMount(){
        this.getEventName();
    }

    getTeamMembers = () => {
        let members = [];
        let teamId = this.state.teamId;
        taskGetTeamService(teamId, true).then(response => {
            let membersId = response.data['members_id'];
            membersId.map(member => {
                members.push({'id': member.id, 'fullName': member.first_name + ' ' + member.last_name});
            });
        });
        this.setState({'members': members, 'team': teamId});
        this.getOwnerName();
    }

    getEventName = () => {
        eventServiceGet(this.state.eventId).then(response => {
            this.setState({
                'eventName': response.data.name,
                'eventDescription': response.data.description,
                'teamId': response.data.team,
                'ownerId': response.data.owner,
                'startAt': response.data.start_at,
                'createdAt': response.data.created_at,
                'updatedAt': response.data.updated_at,
                'duration': response.data.duration,
                'longitude': response.data.longitude,
                'latitude': response.data.latitude,
                'budget': response.data.budget,
                'status': response.data.status,
            });
            this.getTeamMembers(response.data.team);
        });
    };

    getOwnerName = () => {
        getOwner(this.state.ownerId).then(response => {
            const name = (response.data.first_name + ' ' + response.data.last_name);
            this.setState({'owner': name});
        });
    }

    render() {
        return (
            <div>
                {this.state.owner && (
                    <div style={containerStyle}>
                        <Event
                            team={this.state.team}
                            owner={this.state.owner}
                            ownerId={this.state.ownerId}
                            name={this.state.eventName}
                            description={this.state.eventDescription}
                            startAt={this.state.startAt}
                            createdAt={this.state.createdAt}
                            updatedAt={this.state.updatedAt}
                            duration={this.state.duration}
                            longitude={this.state.longitude}
                            latitude={this.state.latitude}
                            budget={this.state.budget}
                            status={this.state.status}
                            id={this.state.eventId}
                        />
                    </div>
                )}
                {this.state.owner && (
                    <div style={containerStyle} >
                        <EventTaskList
                            eventId={this.state.eventId}
                            eventTasks={this.state.tasks}
                            members={this.state.members}
                            teamId={this.state.teamId}
                        />
                    </div>
                )}
            </div>
        );
    }
}
