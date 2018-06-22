import React from 'react';
import {withRouter} from 'react-router-dom';
import { Card, CardHeader, CardText } from 'material-ui/Card';
import {ItemsList} from 'src/containers';

const cardHeaderStyle= {
    fontSize: '25px'
};

const itemsGraphStyle = {
    paddingTop: 10,
    width: '90%',
    maxWidth: '90%'
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
                        <ItemsList
                            curriculumId={this.state.curriculumId}
                            topicId={this.state.topicId}/>
                    </CardText>

                </Card>
            </div>
        );
    }
}

export default withRouter(AssignmentTopicLink);
