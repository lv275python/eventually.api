import React from 'react';
import {withRouter} from "react-router-dom";
import { Card, CardHeader, CardText } from 'material-ui/Card';
import {TopicItemList,} from 'src/containers';

const cardHeaderStyle= {
    fontSize: '25px'
};


const cardTextStyle = {
    color: '#455A64',
    fontSize: '15px'
};

class AssignmentTopicLink extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive,
            curriculumId: this.props.curriculumId,
            topicId: this.props.id,
            isMentor: false
        };
    }

    changeExp = newExpandedState => {
        this.props.change(this.props.id);
    };

    componentWillReceiveProps(nextProps) {
        this.setState({ expanded: nextProps.isActive });
    }

    handleOpen = () => {
        this.setState({ leaveDialogOpen: true });
    };

    handleClose = () => {
        this.setState({ leaveDialogOpen: false });
    };

    render() {

        return (
            <div>
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
                        <TopicItemList
                            curriculumId={this.state.curriculumId}
                            topicId={this.state.topicId}
                            isMentor={this.state.isMentor} />
                    </CardText>

                </Card>
            </div>
        );
    }
}

export default withRouter(AssignmentTopicLink);