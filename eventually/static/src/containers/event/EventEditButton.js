import React from 'react';
import { withRouter } from 'react-router-dom';
import EventEdit from './EventEdit';

const containerStyle = {
    width: '80%',
    margin: '0 auto',
};

const EditEventStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};


class EventEditButton extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={containerStyle}>
                <EventEdit
                    eventId={1}
                    teamId={1}
                    style={EditEventStyle}/>
            </div>
        );
    }
}

export default EventEditButton;
