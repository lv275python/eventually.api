import React from 'react';
import Avatar from 'material-ui/Avatar';
import LibraryBooks from 'material-ui/svg-icons/av/library-books';
import Code from 'material-ui/svg-icons/action/code';
import Group from 'material-ui/svg-icons/social/group';
import PlayArrow from 'material-ui/svg-icons/av/play-arrow';
import RaisedButton from 'material-ui/RaisedButton';
import {Card, CardHeader, CardText, CardActions} from 'material-ui/Card';
import {blue500, yellow600, lime500} from 'material-ui/styles/colors';

const titleStyle = {
    fontWeight: 'bold',
    fontSize: '16px'
};

const cardHeaderStyle = {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer'
};

const textStyle = {
    fontSize: '14px'
};

const actionsStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};

const buttonStyle = {
    width: '17%',
    minWidth: '17%',
    height: '25px'
};

export default class ItemUnit extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: false,
        };
    }

    handleExpandChange = expanded => {
        this.setState({expanded: expanded});
    };

    render() {

        let avatar = null;

        if (this.props.form === 0) {
            avatar = (<Avatar icon={<LibraryBooks />} backgroundColor={yellow600} />);
        } else if (this.props.form === 1) {
            avatar = (<Avatar icon={<Code />} backgroundColor={blue500} />);
        } else {
            avatar = (<Avatar icon={<Group />} backgroundColor={lime500} />);
        }

        return (
            <div>
                <Card expanded={this.state.expanded}
                    onExpandChange={this.handleExpandChange}>
                    <CardHeader
                        title={this.props.name}
                        avatar={avatar}
                        style={cardHeaderStyle}
                        actAsExpander={true}
                        showExpandableButton={true}
                        titleStyle={titleStyle}
                    />
                    <CardText expandable={true}
                        style={textStyle}>
                        {this.props.description}
                    </CardText>
                    <CardActions style={actionsStyle}>
                        <RaisedButton icon={<PlayArrow />}
                            secondary={true}
                            style={buttonStyle}>
                        </RaisedButton>
                    </CardActions>
                </Card>
            </div>
        );
    }
}
