import React from 'react';
import {Card, CardActions, CardHeader, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';
import AssignmentList from './AssignmentList';


const style = {
    color: '#455A64',
    fontSize: '15px'
};
const style1 = {
    fontSize: '25px'
}

export default class TopicItem extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive,
        };
    }

    cangeExp = (newExpandedState) => {
        this.props.change(this.props.id);
    }

    componentWillReceiveProps(nextProps){
        this.setState({expanded: nextProps.isActive});
    }

    render(){
        return(
            <div>
                <Card
                    onExpandChange={this.cangeExp}
                    expanded={this.state.expanded}
                >
                <CardHeader
                    style={style1}
                    title={this.props.title}
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText
                    style={style}
                    expandable={true}>
                    {this.props.description}
                    <AssignmentList/>
                </CardText>
                </Card>
            </div>
        )
    }
}
