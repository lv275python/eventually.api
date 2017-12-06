import React from 'react';
import Divider from 'material-ui/Divider';
import AssignmentLink from './AssignmentLink';
import {assignmentsListService} from './CurriculumService';


const style = {
    'width': '100%',
};


export default class AssignmentList extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={style}>
                    {
                        assignmentsListService().assignments.map(assignment => (
                            <AssignmentLink key={assignment.id.toString()}
                                            title={assignment.title}
                            />
                            )
                        )
                    }
            </div>
        );
    }
}
