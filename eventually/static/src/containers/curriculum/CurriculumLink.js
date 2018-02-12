import React from 'react';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import {withRouter} from 'react-router-dom';
import {getTopicListService} from './CurriculumService';
import {TopicsList, TopicDialog} from 'src/containers';

const cardHeaderStyle = {
    cursor: 'pointer'
};

class CurriculumLink extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            topics: [],
        };
    }

    componentWillMount() {
        getTopicListService(+this.props.id).then(response => {
            this.setState({'topics': response.data['topics']});
        });
    }

    render() {
        return (
            <div>
                <Card>
                    <CardHeader
                        actAsExpander={true}
                        showExpandableButton={true}
                        style={cardHeaderStyle}
                        title={this.props.title}
                        subtitle={this.props.description}
                    />
                    <TopicsList
                        topics={this.state.topics}
                        expandable={true} />
                    <TopicDialog
                        expandable={true}
                        curriculumId = {this.props.id} />
                </Card>
            </div >
        );
    }
}
export default CurriculumLink;

