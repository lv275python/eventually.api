import React from 'react';
import {Card, CardHeader} from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';

const cardHeaderStyle = {
    'display': 'flex',
    'alignItems': 'center',
    'cursor': 'pointer'
};

const titleStyle = {
    'fontWeight': 'bold',
    'fontSize': '18px'
};

export default class MentorItem extends React.Component {

    constructor(props) {
        super(props);
    }

    handleClick = () => {
        this.props.onMentorClick(this.props.id)
    };

    render() {
        return (
            <div>
                <Card>
                    <CardHeader
                        style={cardHeaderStyle}
                        title={`${this.props.firstName} ${this.props.lastName}`}
                        avatar={<Avatar src={"https://robohash.org/" + this.props.avatar}/>}
                        titleStyle={titleStyle}
                        onClick={this.handleClick}
                    />
                </Card>
            </div>
        );
    }
}
