import React from 'react';
import Paper from 'material-ui/Paper';
import UserItem from './UserItem';

export default class UsersList extends React.Component {

    constructor(props) {
        super(props);
    }

    handleItemButtonClick = this.props.onItemButtonClick;

    render() {
        return(
            <div>
                <Paper zDepth={2}>
                    {this.props.students.map(student => (
                        <UserItem
                            key={student.student_id.toString() + student.topic_id.toString()}
                            id={student.student_id}
                            firstName={student.first_name}
                            lastName={student.last_name}
                            topicTitle={student.topic_title}
                            topicId={student.topic_id}
                            avatar={student.avatar}
                            onButtonClick={this.handleItemButtonClick}
                            tabIndex={this.props.tabIndex}
                            getStudentsListData={this.props.getStudentsListData}
                        />
                    ))}
                </Paper>
            </div>
        );
    }
}
