import React from 'react';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';
import {getUserId} from 'src/helper';
import ItemList from '../itemsList/ItemsList';


const cardHeaderStyle = {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer'
};

const titleStyle = {
    fontWeight: 'bold',
    fontSize: '18px'
};

export default class StudentItem extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            userId: this.props.id,
            mentorId: getUserId(),
            topicId: this.props.topicId,
            curriculumId: this.props.curriculumId,
        };
    }

    render() {
        return (
            <Card>
                <CardHeader
                    actAsExpander={true}
                    showExpandableButton={true}
                    style={cardHeaderStyle}
                    title={`${this.props.firstName} ${this.props.lastName}`}
                    subtitle={this.props.topicTitle}
                    avatar={<Avatar src={`https://robohash.org/${this.props.avatar}`}/>}
                    titleStyle={titleStyle}/>
                <CardText expandable={true}>
                    <ItemList
                        curriculumId={this.state.curriculumId}
                        topicId={this.state.topicId}
                        userId={this.state.userId}/>
                </CardText>
            </Card>
        );
    }
}
