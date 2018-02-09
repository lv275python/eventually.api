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
        const data = getTopicListService(+this.props.id);
        this.setState({
            topics: data
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
                        expandable={true} />
                </Card>
            </div >
        );
    }
}
export default CurriculumLink;
