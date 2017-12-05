import React from 'react';
import MentorItem from "./tpmMentorItem";
import Paper from 'material-ui/Paper';

export default class MentorsList extends React.Component {

    constructor(props) {
        super(props);
    }

    handleClick = this.props.onMentorClick;

    render() {
        return(
            <div style={this.props.style}>
                <Paper zDepth={2}>
                    {
                        this.props.mentors.map(mentor => (
                                <MentorItem key={mentor.id.toString()}
                                            id={mentor.id}
                                            firstName={mentor.first_name}
                                            lastName={mentor.last_name}
                                            avatar={mentor.avatar}
                                            onMentorClick={this.handleClick}
                                />
                            )
                        )
                    }
                </Paper>
            </div>
        )
    }
}
