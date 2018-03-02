import React from 'react';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import RaisedButton from 'material-ui/RaisedButton';
import { lightGreen400 } from 'material-ui/styles/colors';
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';
import {getUserId} from 'src/helper';
import ParticipantListDialog from './ParticipantListDialog';
import {getAnswers} from './VoteService';
import {putAnswer} from './VoteService';

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
            teamId: this.props.teamId
        };
    }

    getData = () => {
        getAnswers(this.props.eventId, this.props.voteId).then(response => {
            this.setState(response.data);
        });
    }

    getAnswer = answerId => {
        return this.state.answers.find(function(answer) {
            return answer.id == answerId;
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
                label={answer.text + ' ' + answer.members.length}
                style={styles.radioButton}
                id={answer.id}
            />;
        });
    }

    getPreviousAnswer = userId => {
        return this.state.answers.find(function(answer) {
            return answer.members.includes(userId);
        });
    };

    handleChangeButton = event => {
        const answerId = event.target.id;
        let previousAnswerId = undefined;
        const previousAnswer = this.getPreviousAnswer(getUserId());
        if (previousAnswer) {
            previousAnswerId = previousAnswer.id;
        }

        if (!this.getAnswer(answerId).members.includes(getUserId())) {
            this.submitAnswer(
                this.state.teamId,
                this.props.eventId,
                this.props.voteId,
                answerId
            ).then(response => {
                this.setState({answers: this.state.answers});

                if (previousAnswerId) {
                    this.reSubmitAnswer(
                        this.state.teamId,
                        this.props.eventId,
                        this.props.voteId,
                        previousAnswerId
                    ).then(response => {
                        this.setState({answers: this.state.answers});
                    });
                }
            });
        }
    }

    submitAnswer = (teamId, eventId, voteId, answerId) => {
        let answer = this.getAnswer(answerId);
        answer.members.push(getUserId());

        const members = answer.members;
        return putAnswer(teamId, eventId, voteId, answerId, members);
    };

    reSubmitAnswer = (teamId, eventId, voteId, previousAnswerId) => {
        let previousAnswer = this.getAnswer(previousAnswerId);
        const index = previousAnswer.members.indexOf(getUserId());
        previousAnswer.members.splice(index, 1);

        const members = previousAnswer.members;
        return putAnswer(teamId, eventId, voteId, previousAnswerId, members);
    };

    componentWillMount() {
        this.getData();
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.answers.length != 0) {
            this.setState({
                answers: nextProps.answers
            });
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
                            <RadioButtonGroup name="shipSpeed" defaultSelected="checked"
                                onChange={this.handleChangeButton}>
                                {this.getRadioButtons()}
                            </RadioButtonGroup>
                        </div>
                    </CardActions>
                </Card>
            </div >
        );
    }
}
export default withRouter(CustomVote);
