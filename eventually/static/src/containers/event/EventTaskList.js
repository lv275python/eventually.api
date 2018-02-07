import React from 'react';
import Sortable from 'sortablejs';
import EventTaskItem from './EventTaskItem';
import TaskDialog from './EventTaskDialog';
import { withRouter } from 'react-router-dom';
import {eventTasksServiceGet, eventServiceGet, eventTaskServicePut, taskGetTeamService, getOwner} from './EventService';
import Event from './Event';


const tableStyle = {
    border: '2px solid #B3E5FC',
    borderCollapse: 'separate',
    width: '100%'
};
const thStyle = {
    border: '2px solid #B3E5FC',
    fontWeight: 'normal',
    background: '#00BCD4',
    color: '#FFFFFF',
    padding: '8px'
};
const tdStyle = {
    border: '2px solid #B3E5FC',
    background: '#FFFFFF',
    color: '#000000',
    padding: '8px',
    verticalAlign: 'top'
};
const ulStyle = {
    marginLeft: '0',
    listStyle: 'none',
    counterReset: 'li',
};
const liStyle = {
    position: 'relative',
    marginBottom: '1.5em',
    border: '3px solid #84FFFF',
    padding: '0.6em',
    borderRadius: '4px',
    background: '#B2EBF2',
    color: '#231F20',
    fontFamily: 'Trebuchet MS, Lucida Sans'
};
const containerStyle = {
    width: '80%',
    margin: '0 auto',
};
const TaskDialogStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

export default class EventTaskList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.match.params.eventId,
            teamId: null,
            owner: null,
            event_name: '',
            event_descr: '',
            tasks: [],
            members: []
        };
    }

    componentWillMount(){
        this.getEventTaskItem();
        this.getEventName();
    }

    getEventTaskItem = () => {
        eventTasksServiceGet(this.state.eventId).
            then(response => this.setState({'tasks': response.data.tasks}));
    };

    getTeamMembers = () => {
        let members = [];
        let team_id = this.state.teamId;
        taskGetTeamService(team_id, true).then(response => {
            let members_id = response.data['members_id'];
            members_id.map(member => {
                members.push({'id': member.id, 'full_name': member.first_name + ' ' + member.last_name});

            });
        });
        this.setState({'members': members, 'team': team_id});
        this.getOwnerName();
    }

    getEventName = () => {
        eventServiceGet(this.state.eventId).then(response => {
            this.setState({
                'event_name': response.data.name,
                'event_descr': response.data.description,
                'teamId': response.data.team,
                'ownerId': response.data.owner,
                'start_at': response.data.start_at,
                'created_at': response.data.created_at,
                'updated_at': response.data.updated_at,
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

    sortableGroupDecorator = (sortableGroup) => {
        if (sortableGroup) {
            let options = {
                group: 'Sortable',
                onRemove: evt => {
                    var task_id;
                    this.state.tasks.map(task => {
                        if (evt.item.innerText.search(task.title) > -1) task_id = task.id;
                    });
                    let data = {status: +evt.to.id};
                    eventTaskServicePut(this.state.eventId, task_id, data);
                }
            };

            Sortable.create(sortableGroup, options);
        }
    };

    render() {
        return (
            <div>
                {this.state.owner && (
                    <div style={containerStyle}>
                        <Event
                            team={this.state.team}
                            owner={this.state.owner}
                            name={this.state.event_name}
                            description={this.state.event_descr}
                            start_at={this.state.start_at}
                            created_at={this.state.created_at}
                            updated_at={this.state.updated_at}
                            duration={this.state.duration}
                            longitude={this.state.longitude}
                            latitude={this.state.latitude}
                            budget={this.state.budget}
                            status={this.state.status}
                            id={this.state.eventId}
                        />
                    </div>
                )}
                <table style={tableStyle}>
                    <thead>
                        <tr>
                            <th style={thStyle}>
                                ToDo
                            </th>
                            <th style={thStyle}>
                                InProgress
                            </th>
                            <th style={thStyle}>
                                Done
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style={tdStyle}>
                                <ul  id='0' key='0' type='none' ref={this.sortableGroupDecorator} style={ulStyle}>
                                    {this.state.tasks.map(task => (task.status == 0 &&
                                        <li key={task.id.toString()} key={task.id.toString()} style={liStyle}>
                                            <EventTaskItem
                                                key={task.id.toString()}
                                                id={task.id}
                                                title={task.title}
                                                description={task.description}
                                                assignment_users={task.users}
                                                members={this.state.members}
                                                eventId={this.state.eventId}
                                            />
                                        </li>
                                    ))}
                                </ul>
                            </td>
                            <td style={tdStyle}>
                                <ul  id='1' key='1' type='none' ref={this.sortableGroupDecorator} style={ulStyle}>
                                    {this.state.tasks.map(task => (task.status == 1 &&
                                        <li key={task.id.toString()} style={liStyle}>
                                            <EventTaskItem
                                                key={task.id.toString()}
                                                id={task.id}
                                                title={task.title}
                                                description={task.description}
                                                assignment_users={task.users}
                                                members={this.state.members}
                                                eventId={this.state.eventId}
                                            />
                                        </li>
                                    ))}
                                </ul>
                            </td>
                            <td style={tdStyle}>
                                <ul  id='2' key='2' type='none' ref={this.sortableGroupDecorator} style={ulStyle}>
                                    {this.state.tasks.map(task => (task.status == 2 &&
                                        <li key={task.id.toString()} style={liStyle}>
                                            <EventTaskItem
                                                key={task.id.toString()}
                                                id={task.id}
                                                title={task.title}
                                                description={task.description}
                                                assignment_users={task.users}
                                                members={this.state.members}
                                                eventId={this.state.eventId}
                                            />
                                        </li>
                                    ))}
                                </ul>
                            </td>
                        </tr>
                    </tbody>
                </table>
                {this.state.teamId && (<div style={containerStyle}>
                    <TaskDialog
                        eventId={this.state.eventId}
                        teamId={this.state.teamId}
                        style={TaskDialogStyle}/>
                </div>)}
            </div>
        );
    }
}


