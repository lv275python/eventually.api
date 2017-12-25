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
                            key={student.id.toString()}
                            id={student.id}
                            firstName={student.first_name}
                            lastName={student.last_name}
                            avatar={student.avatar}
                            onButtonClick={this.handleItemButtonClick}
                        />
                    ))}
                </Paper>
            </div>
        );
    }
}
