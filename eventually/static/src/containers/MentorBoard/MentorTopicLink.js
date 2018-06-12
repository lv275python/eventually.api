import React from 'react';
import { withRouter } from 'react-router-dom';
import { Card, CardHeader, CardText } from 'material-ui/Card';
import {getIsMentorService } from '../topicList/TopicServices';
import StudentsMentorList from './StudentsMentor';


const cardTextStyle = {
    color: '#455A64',
    fontSize: '15px'
};

const cardHeaderStyle= {
    fontSize: '25px'
};


class MentorTopicLink extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive,
            isMentor: false,
            topicId: this.props.id,
            curriculumId: this.props.curriculumId,

        };
    }

    changeExp = newExpandedState => {
        this.props.change(this.props.id);
    };

    componentWillMount(){
        getIsMentorService(this.props.curriculumId, this.props.id).then(response => {
            this.setState({isMentor: response.data['is_mentor']});
        });
    }

    componentWillReceiveProps(nextProps) {
        this.setState({ expanded: nextProps.isActive });
    }

    render() {
        let label;
        if (this.state.isMentor === true) {
            label = (
                <Card
                    onExpandChange={this.changeExp}
                    expanded={this.state.expanded}
                >
                    <CardHeader
                        style={cardHeaderStyle}
                        title={this.props.title}
                        id={this.props.id}
                        actAsExpander={true}
                        showExpandableButton={true}
                    />
                    <CardText
                        style={cardTextStyle}
                        expandable={true}>
                        <StudentsMentorList
                            id={this.state.topicId}
                            style={cardTextStyle}
                            expandable={true}
                            actAsExpander={true}
                            showExpandableButton={true}
                            curriculumId={this.state.curriculumId}
                            isMentor={this.state.isMentor}
                        />
                    </CardText>
                </Card>);
        }
        return (
            <div>
                {label}
            </div>
        );
    }
}


export default withRouter(MentorTopicLink);
