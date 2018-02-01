import React from 'react';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import {lightGreen400} from 'material-ui/styles/colors';
import {TopicDialog} from './containers';

const cardTextstyle = {
    color: '#455A64',
    fontSize: '15px'
};

const cardHederStyle= {
    fontSize: '25px'
};

const raiseButtonStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};


export default class TopicItem extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive,
        };
    }

    cangeExp = (newExpandedState) => {
        this.props.change(this.props.id);
    };

    componentWillReceiveProps(nextProps) {
        this.setState({ expanded: nextProps.isActive });
    }

    render() {
        return (
            <div>
                <Card
                    onExpandChange={this.cangeExp}
                    expanded={this.state.expanded}
                >
                    <CardHeader
                        style={cardHederStyle}
                        title={this.props.title}
                        actAsExpander={true}
                        showExpandableButton={true}
                    />

                    <CardText
                        style={cardTextstyle}
                        expandable={true}>
                        {this.props.description}
                        <CardActions>
                            <div style={raiseButtonStyle}>
                                <RaisedButton 
                                    label="Assign" 
                                    backgroundColor={lightGreen400} />
                            </div>
                        </CardActions>
                    </CardText>
                </Card>
            </div>
        );
    }
}
