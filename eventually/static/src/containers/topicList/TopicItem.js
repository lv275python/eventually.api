import React from 'react';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import {lightGreen400} from 'material-ui/styles/colors';
import {TopicDialog} from 'src/containers';
import { postTopicAssignService, getTopicStudentsService, deleteMenteeService, getIsMentorService } from './TopicServices';
import {getUserId} from 'src/helper';

const cardTextStyle = {
    color: '#455A64',
    fontSize: '15px'
};

const cardHeaderStyle= {
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
            isStudent: false,
            leaveDialogOpen:false,
            leaveTopic: false
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

    handleOpen = () => {
        this.setState({ leaveDialogOpen: true });
    };

    handleClose = () => {
        this.setState({ leaveDialogOpen: false });
    };

    handleYes = () => {
        deleteMenteeService (this.props.id).then(response => {
            this.setState({'isStudent': !this.state.isStudent});
            this.handleClose();
        });
    };

    handleNo = () => {
        this.handleClose();
    };

    handleLeave = () => {
        this.handleOpen();
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

        const actionsDialog = [
            <FlatButton
                label="No"
                primary={true}
                onClick={this.handleNo}
            />,
            <FlatButton
                label="Yes"
                primary={true}
                onClick={this.handleYes}
            />,
        ];

        return (
            <div>
                <Card
                    onExpandChange={this.cangeExp}
                    expanded={this.state.expanded}
                >
                    <CardHeader
                        style={cardHeaderStyle}
                        title={this.props.title}
                        actAsExpander={true}
                        showExpandableButton={true}
                    />

                    <CardText
                        style={cardTextStyle}
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
                    <Dialog
                        actions={actionsDialog}
                        modal={true}
                        open={this.state.leaveDialogOpen}
                    >
                        Do you really want to leave this topic?
                    </Dialog>
                </Card>
            </div>
        );
    }
}
