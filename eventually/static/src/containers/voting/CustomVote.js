import React from 'react';
import Dialog from 'material-ui/Dialog';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import Badge from 'material-ui/Badge';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';
import RadioButtonChecked from 'material-ui/svg-icons/toggle/radio-button-checked';
import RaisedButton from 'material-ui/RaisedButton';
import { lightGreen400 } from 'material-ui/styles/colors';
import {getUserId} from 'src/helper';
import {getAnswersWithMembers} from './VoteService';
import {putAnswer} from './VoteService';
import ParticipantListDialog from './ParticipantListDialog';
import DeleteForever from 'material-ui/svg-icons/action/delete-forever';
import {red500} from 'material-ui/styles/colors';
import FlatButton from 'material-ui/FlatButton';
import {deleteCustomVote} from './VoteService';

const raisedButtonDivStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};

const styles = {
    radioButton: {
        marginBottom: 16
    },
    card: {
        borderRadius: '0 20px',
        border: '1px solid #12bbd2',
        width: '80%',
        margin: '10px auto'
    },
};

class CustomVote extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            answers: [],
            teamId: this.props.teamId,
            open: false,
            currentAnswerMembers: [],
            deleteDialogOpen: false,
            voteDeleted: false,
            owner: this.props.owner
        };
    }

    getData = () => {
        getAnswersWithMembers(this.props.eventId, this.props.voteId).then(response => {
            this.setState({
                answers: response.data['answers_members']
            });
        });
    }

    getAnswer = answerId => {
        return this.state.answers.find(function(answer) {
            return answer.id == answerId;
        });
    };

    handleOpen = (event, answerMembers) => {
        this.setState({
            open: Object.keys(answerMembers).length == 0 ? false : true,
            currentAnswerMembers: answerMembers
        });
    };

    handleClose = () => {
        this.setState({
            open: false
        });
    };

    /*check if user is author of suggested topic*/
    ownerCheck = () => {
        if (getUserId() == this.state.owner){
            return true;
        } else {
            return false;
        }
    };

    handleDelete = () => {
        this.handleOpenDelete();
    };

    handleOpenDelete = () => {
        this.setState({ deleteDialogOpen: true });
    };

    handleCloseDelete = () => {
        this.setState({ deleteDialogOpen: false });
    };

    handleYes = () => {
        deleteCustomVote(this.props.teamId, this.props.eventId, this.props.voteId).then(response => {
            this.setState({ voteDeleted: true });
            this.handleCloseDelete();
        });
    };

    handleNo = () => {
        this.handleCloseDelete();
    };

    getRadioButtons() {
        let sortedAnswers = this.state.answers.sort((previousAnswer, nextAnswer) => {
            return previousAnswer.id - nextAnswer.id;
        });

        return sortedAnswers.map(answer => {
            let choice = 'checked' + answer.id;
            if (answer.checked) {
                choice = 'checked';
            }
            return <RadioButton
                key={answer.id.toString()}
                value={choice}
                disabled={this.props.disabled}
                label={
                    <div>
                        <div style={{float: 'left'}}>{answer.text}</div>
                        <Badge
                            key={answer.id.toString()}
                            badgeContent={answer.members.length}
                            badgeStyle={answer.members.length == 0 ? {backgroundColor: '#e4e4e4'} : {}}
                            primary={true}
                            style={{float: 'right', zIndex: '100'}}
                            onClick={event => this.handleOpen(event, answer.members)}
                        >
                        </Badge>
                    </div>
                }
                style={styles.radioButton}
                id={answer.id}/>;
        });
    }

    getPreviousAnswer = userId => {
        return this.state.answers.find(function(answer) {
            return answer.members.find(function(member) {
                return member.id == userId;
            });
        });
    };

    handleChangeButton = event => {
        const answerId = event.target.id;
        let previousAnswerId = undefined;
        const previousAnswer = this.getPreviousAnswer(getUserId());
        if (previousAnswer) {
            previousAnswerId = previousAnswer.id;
        }

        if (!this.getAnswer(answerId).members.find(member => {member.id == getUserId();})) {
            this.submitAnswer(
                this.state.teamId,
                this.props.eventId,
                this.props.voteId,
                answerId
            ).then(response => {
                getAnswersWithMembers(this.props.eventId, this.props.voteId).then(response => {
                    this.setState({answers: response.data['answers_members']});

                    if (previousAnswerId) {
                        this.reSubmitAnswer(
                            this.state.teamId,
                            this.props.eventId,
                            this.props.voteId,
                            previousAnswerId
                        ).then(response => {
                            getAnswersWithMembers(this.props.eventId, this.props.voteId).then(response => {
                                this.setState({answers: response.data['answers_members']});
                            });
                        });
                    }
                });
            });
        }
    };

    submitAnswer = (teamId, eventId, voteId, answerId) => {
        let answer = this.getAnswer(answerId);
        const memberIds = answer.members.map(member => member.id);
        memberIds.push(getUserId());

        return putAnswer(teamId, eventId, voteId, answerId, memberIds);
    };

    reSubmitAnswer = (teamId, eventId, voteId, previousAnswerId) => {
        let previousAnswer = this.getAnswer(previousAnswerId);
        const memberIds = previousAnswer.members.map(member => member.id);
        const index = memberIds.indexOf(getUserId());
        memberIds.splice(index, 1);

        return putAnswer(teamId, eventId, voteId, previousAnswerId, memberIds);
    };

    componentWillMount() {
        this.getData();
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.answers.length != 0) {
            this.setState({answers: nextProps.answers});
        }
    }

    render() {
        const actionsDialog = [
            <FlatButton
                label="Yes"
                key={1}
                primary={true}
                onClick={this.handleYes}
            />,
            <FlatButton
                label="No"
                key={0}
                primary={true}
                onClick={this.handleNo}
            />
        ];
        let deleteButton;
        if(this.ownerCheck()==true){
            deleteButton = (
                <RaisedButton
                    key={0}
                    icon={<DeleteForever color={red500} />}
                    onClick={this.handleDelete} />
            );
        }
        let voteCard;
        if (this.state.voteDeleted == false){
            voteCard = (
                <div>
                    <Card
                        style={styles.card}
                        zDepth={3}
                    >
                        <CardHeader
                            actAsExpander={true}
                            showExpandableButton={false}
                            title={this.props.title}
                        />
                        <CardActions>
                            <div>
                                <RadioButtonGroup
                                    name="shipSpeed"
                                    valueSelected="checked"
                                    onChange={this.handleChangeButton}>
                                    {this.getRadioButtons()}
                                </RadioButtonGroup>
                                <ParticipantListDialog
                                    participants={this.state.currentAnswerMembers}
                                    open={this.state.open}
                                    handleCloseParticipants={this.handleClose}
                                />
                                {deleteButton}
                            </div>
                        </CardActions>
                        <Dialog
                            actions={actionsDialog}
                            modal={true}
                            open={this.state.deleteDialogOpen}>
                            Do you really want to delete this vote?
                        </Dialog>
                    </Card>
                </div >
            );
        } else {
            voteCard = (
                <div>
                    <Card
                        style={styles.card}
                        zDepth={3}
                    >
                        <CardHeader
                            actAsExpander={true}
                            showExpandableButton={false}
                            title={'The vote was successfully deleted'}
                        />
                    </Card>
                </div >
            );
        }
        return (voteCard);
    }
}
export default withRouter(CustomVote);
