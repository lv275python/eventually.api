import React from 'react';
import Sortable from 'sortablejs';
import isEqual from 'lodash/isEqual';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import { eventTaskServicePut, eventTasksServiceGet } from './EventService';
import EventTaskItem from './EventTaskItem';
import TaskDialog from './CreateTaskDialog';


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

const taskDialogStyle = {
    position: 'fixed',
    right: '3%',
    top: '90%'
};

export default class EventTaskList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.eventId,
            tasks: [],
            members: this.props.members,
            openDoneDialog: false,
            tasksChangeStatus: false,
            toDoneTaskId: null,
        };
    }

    componentWillMount(){
        this.getEventTaskItem();
    }

    getEventTaskItem = () => {
        eventTasksServiceGet(this.state.eventId).
            then(response => {
                if (!isEqual(response.data.tasks, this.state.tasks)){
                    this.setState({
                        'tasks': response.data.tasks,
                        'tasksChangeStatus': !this.state.tasksChangeStatus,
                    });
                }
            });
    };

    shouldComponentUpdate(nextProps, nextState){
        return ((this.state.tasks.length == 0 && nextState.tasks.length != 0) ||
            this.state.tasksChangeStatus != nextState.tasksChangeStatus ||
            this.state.openDoneDialog != nextState.openDoneDialog);
    }

    handleOpen = () => {
        this.setState({openDoneDialog: true});
    };

    handleClose = () => {
        this.setState({openDoneDialog: false});
    };

    handleDialogNo = () => {
        this.setState({'tasksChangeStatus': !this.state.tasksChangeStatus});
        this.handleClose();
    };

    handleDialogYes = () => {
        let data = {status: 2};
        eventTaskServicePut(this.state.eventId, this.state.toDoneTaskId, data).
            then(response => this.getEventTaskItem());
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
                        this.setState({'toDoneTaskId': taskId});
                        this.handleOpen();
                    }
                    else {
                        eventTaskServicePut(this.state.eventId, taskId, data).
                            then(response => this.getEventTaskItem());
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
            let strCounter = counter.toString() + this.state.tasksChangeStatus.toString();
            const styleName = ['toDoBodyStyle', 'inProgressBodyStyle', 'doneBodyStyle'];
            taskTable.push(
                <td style={tdStyle[styleName[counter]]} key={strCounter}>
                    <ul id={counter} key={strCounter} type='none' ref={this.sortableGroupDecorator} style={ulStyle}>
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
                                    getEventTaskItem={this.getEventTaskItem}
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
                {this.props.teamId && (<div>
                    <TaskDialog
                        eventId={this.state.eventId}
                        teamId={this.props.teamId}
                        getEventTaskItem={this.getEventTaskItem}
                        style={taskDialogStyle}/>
                </div>)}
            </div>
        );
    }
}


