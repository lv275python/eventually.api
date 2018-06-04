import React from 'react';
import { withRouter } from 'react-router-dom';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import { postTopicAssignService, getTopicStudentsService, deleteMenteeService, getIsMentorService } from '../topicList/TopicServices';
import StudentsMentorList from './StudentsMentor';


const cardTextStyle = {
    color: '#455A64',
    fontSize: '15px'
};

const cardHeaderStyle= {
    fontSize: '25px'
};

const flatButtonStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};


class MentorTopicLink extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive,
            isMentor: false,
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
                        actAsExpander={true}
                        showExpandableButton={true}
                    />
                    <CardText
                        style={cardTextStyle}
                        expandable={true}>
                        <StudentsMentorList
                            style={cardTextStyle}
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
