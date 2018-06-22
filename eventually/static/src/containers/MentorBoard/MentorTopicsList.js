import React from 'react';
import {Card, CardHeader} from 'material-ui/Card';
import {getTopicListService} from '../curriculum/CurriculumService';
import MentorList from './MentorList';

const cardHeaderStyle = {
    cursor: 'pointer'
};

class MentorTopicsList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            topics: [],
            isMentor: false,
        };
    }

    componentWillMount() {
        this.getTopicListData();
    }

    getTopicListData = () => {
        getTopicListService(+this.props.id).then(response => {
            this.setState({
                'topics': response.data['topics']
            });
        });
    };

    render() {
        return (
            <div>
                <Card>
                    <CardHeader
                        actAsExpander={true}
                        showExpandableButton={true}
                        style={cardHeaderStyle}
                        title={this.props.title}
                        subtitle={this.props.description} />
                    <MentorList
                        topics={this.state.topics}
                        expandable={true} />
                </Card>
            </div >
        );
    }
}

export default MentorTopicsList;
