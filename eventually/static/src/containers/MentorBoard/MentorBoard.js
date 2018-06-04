import React from 'react';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import MentorTopicsList from './MentorTopicsList';
import {getCurriculumsService} from './MentorBoardService';


const containerStyle = {
    width: '80%',
    margin: '0 auto',
};

class MentorBoard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            curriculums: [],
        };
    }

    componentWillMount() {
        this.getCurriculumsData();
    }

    getCurriculumsData = () => {
        getCurriculumsService().then(response => {
            this.setState({'curriculums': response.data['curriculums']});
        });

    };


    render() {
        return (
            <div style={containerStyle}>
                <Card>
                    {this.state.curriculums.map( curriculum => (
                        <MentorTopicsList
                            key={curriculum.id.toString()}
                            title={curriculum.name}
                            description={curriculum.description}
                            id={curriculum.id} />
                    ))}
                </Card>
            </div>
        );
    }
}

export default MentorBoard;
