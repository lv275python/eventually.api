import React from 'react';
import { withRouter } from 'react-router-dom';
import TaskDialog from './EventTaskDialog';

const containerStyle = {
    width: '80%',
    margin: '0 auto',
};

const TaskDialogStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};


class AddEventTask extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={containerStyle}>
                <TaskDialog
                    eventId={3}
                    teamId={3}
                    style={TaskDialogStyle}/>
            </div>
        );
    }
}
export default AddEventTask;
