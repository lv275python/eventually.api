import React from 'react';
import {Card, CardHeader} from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';
import RaisedButton from 'material-ui/RaisedButton';
import {lightGreen400} from 'material-ui/styles/colors';
import {getUserId} from 'src/helper';
import {putMentorStudentService, postAssignmentAfterMentorAssignsTopic} from 'src/components';


const cardHeaderStyle = {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer'
};

const titleStyle = {
    fontWeight: 'bold',
    fontSize: '18px'
};

const contentWrapperStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
};

const buttonStyle = {
    marginRight: 10
};

export default class UserItem extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            userId: this.props.id,
            mentorId: getUserId()
        };
    }

    handleAssign = () => {
        const data = {
            'student': this.state.userId,
            'topic': this.props.topicId
        };
        postAssignmentAfterMentorAssignsTopic(data);
        putMentorStudentService(this.state.userId, this.props.topicId, data).then(response => {
            this.props.getStudentsListData();
        });
    };

    handleClick = () => {
        this.props.onButtonClick(this.props.id);
    };

    render() {
        const btn=(this.props.tabIndex===2) ?
            (<RaisedButton label="Assign" backgroundColor={lightGreen400}
                style={buttonStyle} onClick={this.handleAssign}/>):
            (<RaisedButton label="Info" style={buttonStyle} onClick={this.handleClick}/>);

        return (
            <div>
                <Card>
                    <div style={contentWrapperStyle}>
                        <CardHeader
                            style={cardHeaderStyle}
                            title={`${this.props.firstName} ${this.props.lastName}`}
                            subtitle={this.props.topicTitle}
                            avatar={<Avatar src={`https://robohash.org/${this.props.avatar}`}/>}
                            titleStyle={titleStyle}
                            onClick={this.handleClick}
                        />
                        {btn}
                    </div>
                </Card>
            </div>
        );
    }
}
