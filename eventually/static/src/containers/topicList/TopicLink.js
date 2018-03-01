import React from 'react';
import { withRouter } from 'react-router-dom';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import { lightGreen400 } from 'material-ui/styles/colors';
import { TopicDialog } from 'src/containers';
import { postTopicAssignService, getTopicStudentsService, deleteMenteeService, getIsMentorService } from './TopicServices';
import { getUserId } from 'src/helper';


const cardTextStyle = {
    color: '#455A64',
    fontSize: '15px'
};

const cardHeaderStyle= {
    fontSize: '25px'
};

const flatButtonStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};


class TopicLink extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive,
            isMentor: false,
            isRequestedStudent: false,
            isApprovedStudent: false,
            leaveDialogOpen:false,
            leaveTopic: false
        };
    }

    changeExp = newExpandedState => {
        this.props.change(this.props.id);
    };

    componentWillMount(){
        getTopicStudentsService(this.props.id).then(response => {
            this.setState({isRequestedStudent: response.data['is_requested_student'],
                isApprovedStudent: response.data['have_mentor']
            });
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
            this.setState({'isRequestedStudent': !this.state.isRequestedStudent});
        });
    };

    handleLeave = () => {
        this.handleOpen();
    };

    handleViewTopic = () => {
        this.props.history.push(
            '/curriculums/' + this.props.curriculumId + '/topics/' + this.props.id
        );
    };

    handleOpen = () => {
        this.setState({ leaveDialogOpen: true });
    };

    handleClose = () => {
        this.setState({ leaveDialogOpen: false });
    };

    handleYes = () => {
        deleteMenteeService (this.props.id).then(response => {
            this.setState({'isRequestedStudent': !this.state.isRequestedStudent});
            this.handleClose();
        });
    };

    handleNo = () => {
        this.handleClose();
    };

    render() {
        let label, click;
        if (this.state.isApprovedStudent || this.state.isMentor){
            label = 'View Topic';
            click = this.handleViewTopic;
        } else if (this.state.isRequestedStudent){
            label = 'Cancel request';
            click = this.handleLeave;
        } else {
            label = 'Assign to topic';
            click = this.handleAssign;
        }

        const actionsDialog = [
            <FlatButton
                label="Yes"
                primary={true}
                onClick={this.handleYes}
            />,
            <FlatButton
                label="No"
                primary={true}
                onClick={this.handleNo}
            />

        ];

        return (
            <div>
                <Card
                    onExpandChange={this.changeExp}
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
                            <div style={flatButtonStyle}>
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
                        Do you really want to cancel request?
                    </Dialog>
                </Card>
            </div>
        );
    }
}

export default withRouter(TopicLink);
