import React from 'react';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import Badge from 'material-ui/Badge';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';
import RaisedButton from 'material-ui/RaisedButton';
import { lightGreen400 } from 'material-ui/styles/colors';
import {getUserId} from 'src/helper';
import {getAnswersWithMembers} from './VoteService';
import {putAnswer} from './VoteService';
import ParticipantListDialog from './ParticipantListDialog';

const raisedButtonDivStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};

const styles = {
    radioButton: {
        marginBottom: 16
    }
};

class CustomVote extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            answers: [],
            teamId: this.props.teamId,
            open: false,
            currentAnswerMembers: []
        };
    }

    getData = () => {
        getAnswersWithMembers(this.props.eventId, this.props.voteId).then(response => {
            this.setState({answers: response.data['answers_members']});
        });
    }

    getAnswer = answerId => {
        return this.state.answers.find(function(answer) {
            return answer.id == answerId;
        });
    };

    handleOpen = answerMembers => {
        this.setState({
            open: true,
            currentAnswerMembers: answerMembers
        });
    };

    handleClose = () => {
        this.setState({
            open: false
        });
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
                label={
                    <div>
                        <div style={{float: 'left'}}>{answer.text}</div>
                        <Badge
                            key={answer.id.toString()}
                            badgeContent={answer.members.length}
                            primary={true}
                            style={{float: 'right', zIndex: '100'}}
                            onClick={() => this.handleOpen(answer.members)}
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
        return (
            <div>
                <Card>
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
                        </div>
                    </CardActions>
                </Card>
            </div >
        );
    }
}
export default withRouter(CustomVote);
