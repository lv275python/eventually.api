import React from 'react';
import {Card, CardHeader, CardText} from 'material-ui/Card';

const cardHeaderStyle = {
    'display': 'flex',
    'alignItems': 'center',
    'cursor': 'pointer'
};

const titleStyle = {
    'fontWeight': 'bold',
    'fontSize': '16px'
};

const textStyle = {
    'fontSize': '14px'
};

export default class AnswerInfo extends React.Component {

    constructor(props) {
        super(props);
    }


    render() {
        return (
            <div>
                <Card>
                    <CardHeader
                        title={this.props.student_name}
                        style={cardHeaderStyle}
                        titleStyle={titleStyle}
                    />
                    <CardText style={textStyle}>
                        {this.props.student_answer}
                    </CardText>
                </Card>
            </div>
        );
    }
}
