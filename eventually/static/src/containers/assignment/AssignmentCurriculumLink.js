import React from 'react';
import {Card, CardHeader} from 'material-ui/Card';
import {getAssignmentTopicListService} from './AssignmentService';
import AssignmentTopicList from './AssignmentTopicList';

const cardHeaderStyle = {
    cursor: 'pointer'
};

class AssignmentCurriculumLink extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            topics: []
        };
    }

    componentWillMount(){
        this.getTopicListData();
    }

    getTopicListData = () => {
        getAssignmentTopicListService(+this.props.id).then(response => {
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
                    <AssignmentTopicList
                        topics={this.state.topics}
                        expandable={true} />
                </Card>
            </div >
        );
    }

}

export default AssignmentCurriculumLink;
