import React from 'react';
// import CurriculumMentors from '../curriculumMentors/CurriculumMentors';
import MessagesList from './MessagesList';
import {messagesListService, mentorsService} from './messagesBarService';

const mentorsListStyle = {
    paddingTop: 10
};

export default class MessagesBar extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isMessagesList: false
        };
    }

    componentWillMount() {
        this.setState({
            mentors: mentorsService().mentors
        });
    }

    handleMentorClick = mentorId => {
        this.setState({
            isMessagesList: true,
            messages: messagesListService(mentorId).messages
        });
    };

    render() {
        let messagesList = this.state.isMessagesList ? <MessagesList messages={this.state.messages} /> : null;

        return (
            <div style={this.props.style}>
                <CurriculumMentors
                    style={mentorsListStyle}
                    mentors={this.state.mentors}
                    onMentorClick={this.handleMentorClick}/>
                {messagesList}
            </div>
        );
    }
}
