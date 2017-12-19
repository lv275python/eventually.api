import React from 'react';
import AssignmentInfo from './AssignmentInfo';
import AnswerInfo from './AnswerInfo';
import MessagesBar from './MessagesBar';
import SetGrade from './SetGrade';
import {itemInfoService,answerInfoService} from './MentorItemService';

const profileStyle = {
    display: 'flex',
    justifyContent: 'space-between'
};

const assignmentStyle = {
    'width': '49%'
};


const messagesBarStyle = {
    'width': '49%'
};

export default class MentorItem extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            item_info:{},
            answer_info:{},
        };
    }

    componentWillMount() {
        this.setState({item_info: itemInfoService().item_info,
            answer_info: answerInfoService().answer_info});
    }

    render() {
        return (
            <div style={profileStyle}>
                <div style={assignmentStyle}>
                    <AssignmentInfo 
                        name={this.state.item_info.item_name} 
                        text={this.state.item_info.text}/>
                    <AnswerInfo
                        student_name={this.state.answer_info.student_name}
                        student_answer={this.state.answer_info.student_answer}/>
                    <SetGrade/>
                </div>
                <MessagesBar style={messagesBarStyle} />
            </div>
        );
    }
}
