import React from 'react';
import {MessagesBar, ProgressGraph} from 'src/containers';
import {StudentsTabsList} from 'src/components';

const mentorDashboardStyle = {
    display: 'flex',
    justifyContent: 'space-between'
};

const usersListGraphWrapperStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '70%'
};

const usersListStyle = {
    width: '95%',
    maxWidth: '95%'
};

const progressGraphStyle = {
    width: '85%',
    maxWidth: '85%'
};

const messagesBarStyle = {
    width: '30%',
    position: 'relative'
};

export default class MentorDashboard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div style={mentorDashboardStyle}>
                <div style={usersListGraphWrapperStyle}>
                    <ProgressGraph style={progressGraphStyle} />
                    <StudentsTabsList style={usersListStyle} />
                </div>
                <MessagesBar
                    style={messagesBarStyle}
                    location={this.props.location.pathname.slice(1)}
                    expandedWidth={'30%'}
                    wrappedWidth={'5%'}
                    type='mentor'
                />
            </div>
        );
    }
}
