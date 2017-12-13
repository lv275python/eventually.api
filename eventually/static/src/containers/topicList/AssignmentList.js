import React from 'react';
import AssignmentItem from './AssignmentLink';
import {assignmentsListService} from './CurriculumService';

const style = {
    'width': '100%',
};

export default class AssignmentList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            assignments: []
        };
    }

    componentWillMount() {
        this.setState({
            assignments: assignmentsListService().assignments
        });
    }

    render() {
        return (
            <div style={style}>
                {
                    this.state.assignments.map(assignment => (
                        <AssignmentItem
                            key={assignment.id.toString()}
                            title={assignment.title}
                            id={assignment.id}
                        />)
                    )
                }
            </div>
        );
    }
}
