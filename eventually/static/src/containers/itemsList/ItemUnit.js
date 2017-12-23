import React from 'react';
import Avatar from 'material-ui/Avatar';
import LibraryBooks from 'material-ui/svg-icons/av/library-books';
import Code from 'material-ui/svg-icons/action/code';
import Group from 'material-ui/svg-icons/social/group';
import FlatButton from 'material-ui/FlatButton';
import {Card, CardHeader, CardText, CardActions} from 'material-ui/Card';
import {blue500, yellow600, lime500} from 'material-ui/styles/colors';

const titleStyle = {
    fontWeight: 'bold',
    fontSize: '16px'
};

const cardHeaderStyle = {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
    fontSize: '14px',
};

const cardTextStyle = {
    fontSize: '14px'
};

const actionsStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};

export default class ItemUnit extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive
        };
    }

    handleClick = () => {
        this.props.onClick(this.props.id);
    };

    componentWillReceiveProps(nextProps) {
        this.setState({
            expanded: nextProps.isActive
        });
    }

    render() {

        let avatar = null,
            controlButton = (
                <FlatButton
                    label="Send Answer"
                    primary={true}
                    onClick={this.props.onModalOpen}
                />
            );

        if (this.props.form === 0) {
            avatar = (<Avatar icon={<LibraryBooks />} backgroundColor={yellow600} />);
            controlButton = <FlatButton label="Done" secondary={true} />;
        } else if (this.props.form === 1) {
            avatar = (<Avatar icon={<Code />} backgroundColor={blue500} />);
        } else  if (this.props.form === 2) {
            avatar = (<Avatar icon={<Group />} backgroundColor={lime500} />);
        }

        return (
            <div>
                <Card
                    expanded={this.state.expanded}
                    onExpandChange={this.handleClick}
                >
                    <CardHeader
                        title={this.props.name}
                        avatar={avatar}
                        style={cardHeaderStyle}
                        actAsExpander={true}
                        showExpandableButton={true}
                        titleStyle={titleStyle}
                    />
                    <CardText expandable={true}
                        style={cardTextStyle}>
                        {this.props.description}
                        <CardActions style={actionsStyle}>
                            {controlButton}
                        </CardActions>
                    </CardText>
                </Card>
            </div>
        );
    }
}
