import React from 'react';
import { getCurriculumsService } from './CurriculumService';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import CurriculumLink from './CurriculumLink';
import CurriculumDialog from './CurriculumDialog';

const containerStyle = {
    width: '80%',
    margin: '0 auto',
};

const CurriculumDialogStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};


class CurriculumList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            curriculums: []
        };

    }

    componentWillMount() {
        getCurriculumsService().then(response => {
            this.setState({'curriculums': response.data['curriculums']});
        });
    }


    render() {
        return (
            <div style={containerStyle}>
                {
                    this.state.curriculums.map(curriculum => (
                        <CurriculumLink
                            key={curriculum.id.toString()}
                            title={curriculum.name}
                            description={curriculum.description}
                            id={curriculum.id}
                        />)
                    )
                }
                <CurriculumDialog style={CurriculumDialogStyle}/>
            </div>
        );
    }
}
export default CurriculumList;
