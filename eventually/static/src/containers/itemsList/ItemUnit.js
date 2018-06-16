import React from 'react';
import Avatar from 'material-ui/Avatar';
import LibraryBooks from 'material-ui/svg-icons/av/library-books';
import Code from 'material-ui/svg-icons/action/code';
import Book from 'material-ui/svg-icons/action/book';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import {Card, CardHeader, CardText, CardActions} from 'material-ui/Card';
import {blue500, yellow600, lime500} from 'material-ui/styles/colors';
import Dialog from 'material-ui/Dialog';
import {checkUserAnswer, dismissUserAnswer, sendAnswerToUser} from 'src/containers/MentorBoard/MentorBoardService';
import {putAssignmentService, updatePracticalAssignmentService} from './itemsListService';
import {AssignmentUpload} from 'src/containers';


const titleStyle = {
    fontWeight: 'bold',
    fontSize: '16px'
};

const inputStyle = {
    width: '100%',
};

const cardHeaderStyle = {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
    fontSize: '14px',
};

const cardTextStyle = {
    fontSize: '14px'
};

const actionsStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};

const STATUS_REQUESTED = 0;
const STATUS_IN_PROCESS = 1;
const STATUS_DONE = 2;

const FORM_THEORETIC = 0;
const FORM_PRACTICE = 1;
const FORM_GROUP = 2;

export default class ItemUnit extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive,
            grade: this.props.grade,
            handleCheckDialog: false,
            status: this.props.status,
            handleMentorAnswer: false,
            textAnswer: '',
            userId: this.props.userId,
        };
    }

    handleClick = () => {
        this.props.onClick(this.props.id);
    };


    handleOpenCheck = () => {
        this.setState({
            handleCheckDialog: true,
        });
    };

    handleCloseCheck = () => {
        const id = this.props.id;
        dismissUserAnswer(id, 1).then(response => {
            this.setState({
                handleCheckDialog: false,
                handleMentorAnswer: true,
            });
        });
    };

    handleSubmit = () => {
        const id = this.props.assignmentId;
        checkUserAnswer(id, true).then(response => {
            this.setState({
                handleCheckDialog: false
            });
        });
    };

    handleAnswer = event => {
        this.setState({
            textAnswer: event.target.value,
        });
    };

    handleSendAnswer = () => {
        const userId = this.state.userId;
        let message = this.state.textAnswer;
        sendAnswerToUser(message, userId);
        this.setState({
            handleMentorAnswer: false,
        });
    };
    handleStartAssignment = () => {
        const assignmentId = this.props.assignmentId;
        putAssignmentService(assignmentId, STATUS_IN_PROCESS).then(response => {
            this.updateStatus(response.status, STATUS_IN_PROCESS)
        });
    };

    handleEndAssignment = () => {
        const assignmentId = this.props.assignmentId;
        putAssignmentService(assignmentId, STATUS_DONE, true).then(response => {
            this.updateStatus(response.status, STATUS_DONE);
            this.props.remountItems();
        });
    };

    componentWillReceiveProps(nextProps) {
        this.setState({
            expanded: nextProps.isActive
        });
    }

    updateStatus = (status, assignmentStatus) => {
        if (status === 200){
            this.setState({
                status: assignmentStatus
            });
        }
    };

    updatePracticalAssignment = (fileKey) => {
        updatePracticalAssignmentService(this.props.assignmentId, fileKey).then(response => {
                this.updateStatus(response.status, STATUS_DONE)
            });
    };

    render() {
        const actionsDialog = [
            <FlatButton
                label="Yes"
                key={1}
                primary={true}
                onClick={this.handleSubmit}
            />,
            <FlatButton
                label="No"
                key={0}
                primary={true}
                onClick={this.handleCloseCheck}
            />
        ];


        const actionAnswerDialog = [
            <FlatButton
                label="Send"
                key={1}
                primary={true}
                onClick={this.handleSendAnswer}
            />
        ];

        let controlButton;
        let avatar = null;
        if (this.props.form === FORM_THEORETIC) {
            avatar = (<Avatar icon={<LibraryBooks />}
                backgroundColor={yellow600} />);

        } else if (this.props.form === FORM_PRACTICE) {
            avatar = (<Avatar icon={<Code />}
                backgroundColor={blue500} />);

        } else  if (this.props.form === FORM_GROUP) {
            avatar = (<Avatar icon={<Book />}
                backgroundColor={lime500} />);
        }
        if (this.props.isMentor === true) {
            controlButton = (
                <FlatButton
                    label="Check Answer"
                    primary={true}
                    onClick={this.handleOpenCheck}
                />
            );
            if (this.state.status === STATUS_IN_PROCESS) {
                controlButton = <FlatButton
                    label="In process"
                    disabled/>;
            } else if (this.state.status === STATUS_REQUESTED) {
                controlButton = <FlatButton
                    label="Not started"
                    disabled/>;
            }
        } else {
            controlButton = <FlatButton
                label="Start"
                onClick={this.handleStartAssignment}
                backgroundColor={lime500}/>;

            if (this.state.status === STATUS_IN_PROCESS) {
                if (this.props.form === FORM_THEORETIC || this.props.form === FORM_GROUP) {
                    controlButton = <FlatButton
                        label="Done"
                        onClick={this.handleEndAssignment}
                        secondary={true}/>;

                } else if (this.props.form === FORM_PRACTICE) {
                    controlButton = <AssignmentUpload
                        assignment_id={this.props.assignmentId}
                        updatePracticalAssignment = {this.updatePracticalAssignment}
                        curriculumId = {this.props.curriculumId}
                        topicId = {this.props.topicId}
                        itemId = {this.props.id}
                    />;
                }

            } else if (this.state.status === STATUS_DONE) {
                controlButton = <FlatButton
                    label="Completed"
                    backgroundColor={yellow600}
                    disabled={true}/>;
            }
        }

        return (
            <div>
                <Card
                    expanded={this.state.expanded}
                    onExpandChange={this.handleClick}
                >
                    <CardHeader
                        title={this.props.name}
                        avatar={avatar}
                        style={cardHeaderStyle}
                        actAsExpander={true}
                        showExpandableButton={true}
                        titleStyle={titleStyle}
                    />
                    <CardText expandable={true}
                        style={cardTextStyle}>
                        {this.props.description}
                        <CardActions style={actionsStyle}>
                            {controlButton}
                        </CardActions>
                    </CardText>
                </Card>
                <Dialog
                    actions = {actionAnswerDialog}
                    open={this.state.handleMentorAnswer}>
                    <TextField
                        hintText={'Write your answer here'}
                        style={inputStyle}
                        multiLine={true}
                        id={'answer'}
                        label={'Your answer'}
                        autoFocus
                        onChange={this.handleAnswer}
                    />
                </Dialog>
                <Dialog
                    actions={actionsDialog}
                    modal={true}
                    open={this.state.handleCheckDialog}>
                    Approve this assignment?
                </Dialog>
            </div>
        );
    }
}
