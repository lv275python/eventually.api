import React from 'react';
import StudentItem from './tmpStudentItem';
import MessagesList from './MessagesList';
import {messagesListService, studentService} from './MentorItemService';

const mentorsListStyle = {
    'paddingTop': 10
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
            student: studentService().student
        });
    }

    handleStudentClick = studentId => {
        this.setState({
            isMessagesList: true,
            messages: messagesListService(studentId).messages
        });
    };

    render() {
        let messagesList = this.state.isMessagesList ? <MessagesList messages={this.state.messages} /> : null;

        return (
            <div style={this.props.style}>
                <StudentItem 
                    style={mentorsListStyle} 
                    firstName={this.state.student.firstName}
                    lastName={this.state.student.lastName}
                    id={this.state.student.id}
                    avatar={this.state.student.avatar}
                    onStudentClick={this.handleStudentClick}/>
                {messagesList}
            </div>
        );
    }
}
