import React from 'react';
import Sortable from 'sortablejs';
import EventTaskItem from './EventTaskItem';
import {eventTasksServiceGet, eventServiceGet, eventTaskServicePut, taskGetTeamService} from './EventTaskService';

export default class EventTaskList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.match.params.eventId,
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

    getTeamMembers = team_id => {
        let members = [];
        taskGetTeamService(team_id, true).then(response => {
            let members_id = response.data['members_id'];
            members_id.map(member => {
                members.push({'id': member.id, 'full_name': member.first_name + ' ' + member.last_name});
            });
        });
        this.setState({'members': members});
    }

    getEventName = () => {
        eventServiceGet(this.state.eventId).then(response => {
            this.setState({'event_name': response.data.name,
                'event_descr': response.data.description
            });
            this.getTeamMembers(response.data.team);
        });
    };

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
        var tableStyle = {
            border: '2px solid #B3E5FC',
            borderCollapse: 'separate',
            width: '100%'
        };
        var thStyle = {
            border: '2px solid #B3E5FC',
            fontWeight: 'normal',
            background: '#00BCD4',
            color: '#FFFFFF',
            padding: '8px'
        };
        var tdStyle = {
            border: '2px solid #B3E5FC',
            background: '#FFFFFF',
            color: '#000000',
            padding: '8px',
            verticalAlign: 'top'
        };
        var ulStyle = {
            marginLeft: '0',
            listStyle: 'none',
            counterReset: 'li',
        };
        var liStyle = {
            position: 'relative',
            marginBottom: '1.5em',
            border: '3px solid #84FFFF',
            padding: '0.6em',
            borderRadius: '4px',
            background: '#B2EBF2',
            color: '#231F20',
            fontFamily: 'Trebuchet MS, Lucida Sans'
        };
        return (
            <div>
                <h1>
                    {this.state.event_name}
                </h1>
                <h3>
                    {this.state.event_descr}
                </h3>
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
                                <ul  id='0' type='none' ref={this.sortableGroupDecorator} style={ulStyle}>
                                    {this.state.tasks.map(task => (task.status == 0 &&
                                        <li style={liStyle}>
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
                                <ul  id='1' type='none' ref={this.sortableGroupDecorator} style={ulStyle}>
                                    {this.state.tasks.map(task => (task.status == 1 &&
                                        <li style={liStyle}>
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
                                <ul  id='2' type='none' ref={this.sortableGroupDecorator} style={ulStyle}>
                                    {this.state.tasks.map(task => (task.status == 2 &&
                                        <li style={liStyle}>
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
            </div>
        );
    }
}

