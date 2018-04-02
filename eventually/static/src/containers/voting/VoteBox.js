import React from 'react';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import StandardVote from './StandardVote';
import CustomVote from './CustomVote';
import CreateCustomVote from './CreateCustomVote';
import { getVotes } from './VoteService';

const containerStyle = {
    width: '60%',
    margin: '0 auto'
};

class VoteBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.match.params.eventId,
            votes: [],
            teamId: this.props.location.state.teamId,
            disabled: this.props.location.state.startAt * 1000 < (new Date()).getTime()
        };
    }

    getData = () => {
        getVotes(this.state.eventId).then(response => {
            let sortedVotes = response.data.votes.reverse();
            let votes = sortedVotes.map(vote => {
                vote['answers'] = [];
                return vote;
            });
            this.setState({ votes: votes });
        });
    };

    getStandardVoteComponent() {
        const vote = this.state.votes.find(vote => {
            return vote.title === 'Would you like to visit?';
        });
        if (vote) {
            return <StandardVote
                key={vote.id.toString()}
                title={vote.title}
                eventId={this.state.eventId}
                voteId={vote.id}
                teamId={this.state.teamId}
                disabled={this.state.disabled}
            />;
        }
    }

    getCustomVoteComponents() {
        const votes = this.state.votes.filter(vote => {
            return vote.title !== 'Would you like to visit?';
        });
        return votes.map(vote => {
            return <CustomVote
                key={vote.id.toString()}
                title={vote.title}
                eventId={this.state.eventId}
                voteId={vote.id}
                teamId={this.state.teamId}
                answers={vote.answers}
                disabled={this.state.disabled}
            />;
        });
    }

    componentWillMount() {
        this.getData();
    }

    addVote = (newVote) => {
        this.state.votes.unshift(newVote);
        this.setState({
            votes: this.state.votes
        });
    };

    addAnswer = (newVote) => {
        let votes = this.state.votes;
        for (let i = 0; i < votes.length; i++) {
            if (votes[i].id == newVote.id) {
                votes[i] = newVote;
                break;
            }
        }
        this.setState({
            votes: votes
        });
    };

    render() {
        return (
            <div style={containerStyle}>
                {this.getStandardVoteComponent()}
                <br />
                {this.getCustomVoteComponents()}
                <br />
                <CreateCustomVote
                    event={this.state.eventId}
                    addVote={this.addVote}
                    addAnswer={this.addAnswer}
                    disabled={this.state.disabled}
                />
            </div>
        );
    }
}

export default VoteBox;
