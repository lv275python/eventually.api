import React from 'react';
import MentorItem from './CurriculumMentorItem';
import Paper from 'material-ui/Paper';

export default class CurriculumMentors extends React.Component {

    constructor(props) {
        super(props);
    }

    handleMentorClick = this.props.onMentorClick;

    render() {
        return(
            <div style={this.props.style}>
                <Paper zDepth={2}>
                    {this.props.mentors.map(mentor => (
                        <MentorItem
                            key={mentor.id.toString()}
                            id={mentor.id}
                            firstName={mentor.first_name}
                            lastName={mentor.last_name}
                            avatar={mentor.avatar}
                            onMentorClick={this.handleMentorClick}
                        />
                    ))}
                </Paper>
            </div>
        );
    }
}
