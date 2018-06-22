import React from 'react';
import StudentItem from './StudentItem.js';

export default class StudentList extends React.Component {

    constructor(props) {
        super(props);

    }

    render()
    {
        return(
            <div>
                {this.props.students.map(student => (
                    <StudentItem
                        key={student.student_id.toString() + student.topic_id.toString()}
                        id={student.student_id}
                        firstName={student.first_name}
                        lastName={student.last_name}
                        topicTitle={student.topic_title}
                        topicId={student.topic_id}
                        avatar={student.avatar}
                        tabIndex={this.props.tabIndex}
                        getStudentsListData={this.props.getStudentsListData}
                        curriculumId = {this.props.curriculumId}
                        isMentor={this.props.isMentor}
                    />
                ))}
            </div>
        );
    }
}
