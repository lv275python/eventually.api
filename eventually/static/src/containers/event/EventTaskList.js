import React from 'react';
import Sortable from 'sortablejs';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import { eventTaskServicePut } from './EventService';
import EventTaskItem from './EventTaskItem';


const tableStyle = {
    width: '100%'
};

const thStyle = {
    toDoHeadStyle: {
        fontWeight: 'normal',
        background: '#BDBDBD',
        color: '#000000',
        padding: '8px',
        width: '33%'
    },
    inProgressHeadStyle: {
        fontWeight: 'normal',
        background: '#D4E157',
        color: '#000000',
        padding: '8px',
        width: '33%'
    },
    doneHeadStyle: {
        fontWeight: 'normal',
        background: '#66BB6A',
        color: '#000000',
        padding: '8px',
        width: '33%'
    },
};

const tdStyle = {
    toDoBodyStyle: {
        background: '#F5F5F5',
        color: '#000000',
        padding: '8px',
        verticalAlign: 'top'
    },
    inProgressBodyStyle: {
        background: '#FFF9C4',
        color: '#000000',
        padding: '8px',
        verticalAlign: 'top'
    },
    doneBodyStyle: {
        background: '#C8E6C9',
        color: '#000000',
        padding: '8px',
        verticalAlign: 'top'
    }
};

const ulStyle = {
    marginLeft: '0',
    listStyle: 'none',
    counterReset: 'li',
    minHeight: '300px',
    padding: '0px',
};

const liStyle = {
    position: 'relative',
    marginBottom: '1.5em',
    padding: '0.6em',
    color: '#231F20',
    fontFamily: 'Trebuchet MS, Lucida Sans'
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
            eventId: this.props.eventId,
            tasks: this.props.eventTasks,
            members: this.props.members,
            openDoneDialog: false,
            tasksChangeStatus: 0,
            toDoneTaskId: null
        };
    }

    shouldComponentUpdate(nextProps, nextState){
        return this.props != nextProps || this.state.openDoneDialog != nextState.openDoneDialog || (this.state.tasks == nextState.tasks && this.state.toDoneTaskId == nextState.toDoneTaskId);
    }

    handleOpen = () => {
        this.setState({openDoneDialog: true});
        return true;
    };

    handleClose = () => {
        this.setState({openDoneDialog: false});
    };

    handleDialogNo = () => {
        this.setState({'tasksChangeStatus': this.state.tasksChangeStatus+1});
        this.handleClose();
    };

    handleDialogYes = () => {
        let data = {status: 2};
        eventTaskServicePut(this.state.eventId, this.state.toDoneTaskId, data);
        let nextTasks = this.state.tasks.map(
            task => {
                if (task.id == this.state.toDoneTaskId) task.status = 2;
                return task;
            }
        );
        this.setState({tasks: nextTasks});
        this.setState({'tasksChangeStatus': this.state.tasksChangeStatus+1});
        this.handleClose();
    };

    sortableGroupDecorator = sortableGroup => {
        if (sortableGroup) {
            let options = {
                group: 'Sortable',
                animation: 150,
                onRemove: evt => {
                    let taskId = evt.item.id;
                    let data = {status: +evt.to.id};
                    if (evt.to.id == '2') {
                        this.handleOpen(taskId);
                        this.setState({'toDoneTaskId': taskId});
                    }
                    else {
                        eventTaskServicePut(this.state.eventId, taskId, data);
                        let nextTasks = this.state.tasks.map(
                            task => {
                                if (task.id == taskId) task.status = +evt.to.id;
                                return task;
                            }
                        );
                        this.setState({tasks: nextTasks});
                        this.setState({'tasksChangeStatus': this.state.tasksChangeStatus+1});
                    }
                },
            };
            Sortable.create(sortableGroup, options);
        }
    };

    render() {
        const actions = [
            <FlatButton
                label="No"
                primary={true}
                onClick={this.handleDialogNo}
            />,
            <FlatButton
                label="Yes"
                primary={true}
                onClick={this.handleDialogYes}
            />,
        ];

        let taskTable = [];
        for(let counter = 0; counter < 3; counter++){
            let strCounter = counter.toString() + this.state.tasksChangeStatus;
            const styleName = ['toDoBodyStyle', 'inProgressBodyStyle', 'doneBodyStyle'];
            taskTable.push(
                <td style={tdStyle[styleName[counter]]} key={strCounter}>
                    <ul  id={counter} key={strCounter} type='none' ref={this.sortableGroupDecorator} style={ulStyle}>
                        {this.state.tasks.map(task => (task.status == counter &&
                            <li key={task.id.toString()} id={task.id.toString()} style={liStyle}>
                                <EventTaskItem
                                    key={task.id.toString()}
                                    id={task.id}
                                    title={task.title}
                                    description={task.description}
                                    assignmentUsers={task.users}
                                    members={this.state.members}
                                    eventId={this.state.eventId}
                                    status={task.status}
                                />
                            </li>
                        ))}
                    </ul>
                </td>
            );
        }

        return (
            <div>
                <table style={tableStyle}>
                    <thead>
                        <tr>
                            <th style={thStyle.toDoHeadStyle}>
                                ToDo
                            </th>
                            <th style={thStyle.inProgressHeadStyle}>
                                InProgress
                            </th>
                            <th style={thStyle.doneHeadStyle}>
                                Done
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            {taskTable}
                        </tr>
                    </tbody>
                </table>
                <Dialog
                    title="Are you sure?"
                    actions={actions}
                    modal={true}
                    open={this.state.openDoneDialog}
                >
                    Do you really want to change status of this task to Done?
                </Dialog>
            </div>
        );
    }
}


