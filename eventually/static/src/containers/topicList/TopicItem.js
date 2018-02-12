import React from 'react';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import {lightGreen400} from 'material-ui/styles/colors';
import {TopicDialog} from 'src/containers';
import { postTopicAssignService, getTopicStudentsService, deleteMenteeService, getIsMentorService } from './TopicServices';
import {getUserId} from 'src/helper';

const cardTextstyle = {
    color: '#455A64',
    fontSize: '15px'
};

const cardHederStyle= {
    fontSize: '25px'
};

const raiseButtonStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};


export default class TopicItem extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive,
            isAuthor: false,
            isMentor: false,
            isStudent: false
        };
    }

    cangeExp = (newExpandedState) => {
        this.props.change(this.props.id);
    };

    componentWillMount(){
        getTopicStudentsService(this.props.id).then(response => {
            this.setState({isStudent: response.data['is_student']});
        });
        getIsMentorService(this.props.curriculumId, this.props.id).then(response => {
            this.setState({isMentor: response.data['is_mentor']});
        });
    }

    componentWillReceiveProps(nextProps) {
        this.setState({ expanded: nextProps.isActive });
    }

    handleAssign = () => {
        const data = {'topicId': this.props.id};
        postTopicAssignService(data).then(response => {
            this.setState({'isStudent': !this.state.isStudent});
        });
    };

    handleLeave = () => {
        deleteMenteeService (this.props.id).then(response => {
            this.setState({'isStudent': !this.state.isStudent});
        });
    };

    render() {
        let label, click;
        if (this.state.isStudent){
            label = 'Leave topic';
            click = this.handleLeave;
        } else if (this.state.isMentor){
            label = 'Edit topic';
            click = this.handleEdit;
        } else {
            label = 'Assign to topic';
            click = this.handleAssign;
        }

        return (
            <div>
                <Card
                    onExpandChange={this.cangeExp}
                    expanded={this.state.expanded}
                >
                    <CardHeader
                        style={cardHederStyle}
                        title={this.props.title}
                        actAsExpander={true}
                        showExpandableButton={true}
                    />

                    <CardText
                        style={cardTextstyle}
                        expandable={true}>
                        {this.props.description}
                        <CardActions>
                            <div style={raiseButtonStyle}>
                                <FlatButton
                                    label={label}
                                    backgroundColor={lightGreen400}
                                    onClick={click} />
                            </div>
                        </CardActions>
                    </CardText>
                </Card>
            </div>
        );
    }
}
