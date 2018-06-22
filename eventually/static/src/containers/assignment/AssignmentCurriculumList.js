import React from 'react';
import { getAssignmentCurriculumService } from './AssignmentService';
import AssignmentCurriculumLink from './AssignmentCurriculumLink';

const containerStyle = {
    width: '80%',
    margin: '0 auto',
};


class AssignmentCurriculumList extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            curriculums: []
        };
    }

    componentWillMount(){
        this.getAssignmentCurriculumData();
    }

    getAssignmentCurriculumData(){
        getAssignmentCurriculumService().then(response => {
            this.setState({'curriculums': response.data['curriculums']});
        });
    }

    render() {
        return (
            <div style={containerStyle}>
                {this.state.curriculums.map(curriculum => (
                    <AssignmentCurriculumLink
                        key={curriculum.id.toString()}
                        title={curriculum.name}
                        description={curriculum.description}
                        id={curriculum.id}/>
                ))}
            </div>
        );
    }

}

export default AssignmentCurriculumList;
