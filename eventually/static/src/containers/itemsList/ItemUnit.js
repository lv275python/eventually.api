import React from 'react';
import Avatar from 'material-ui/Avatar';
import LibraryBooks from 'material-ui/svg-icons/av/library-books';
import Code from 'material-ui/svg-icons/action/code';
import Book from 'material-ui/svg-icons/action/book';
import FlatButton from 'material-ui/FlatButton';
import {Card, CardHeader, CardText, CardActions} from 'material-ui/Card';
import {blue500, yellow600, lime500} from 'material-ui/styles/colors';
import {putAssignmentService} from './itemsListService';


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

const STATUS_IN_PROCESS = 1;
const FORM_THEORETIC = 0;
const FORM_PRACTICE = 1;
const FORM_GROUP = 2;

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

    handleStartAssignment = () => {
        putAssignmentService(this.props.assignmenId, {'status': STATUS_IN_PROCESS})//.then(response => {
        //     ;
        // })
    };

    componentWillReceiveProps(nextProps) {
        this.setState({
            expanded: nextProps.isActive
        });
    }

    render() {

        let avatar = null,
            controlButton = <FlatButton
                            label="Start assignment"
                            primary={true}
                            onClick={this.handleStartAssignment}/>;

        if (this.props.form === FORM_THEORETIC) {
                avatar = (<Avatar icon={<LibraryBooks />}
                                  backgroundColor={yellow600} />);

        } else if (this.props.form === FORM_PRACTICE) {
            avatar = (<Avatar icon={<Code />}
                              backgroundColor={blue500} />);

        } else  if (this.props.form === 2) {
            avatar = (<Avatar icon={<Book />}
                              backgroundColor={lime500} />);
        }

        if (this.props.status === STATUS_IN_PROCESS) {
            if (this.props.form === FORM_THEORETIC) {
                controlButton = <FlatButton
                                label="Done"
                                secondary={true}/>;

            } else if (this.props.form === FORM_PRACTICE) {
                controlButton = <FlatButton
                                label="Send Answer"
                                primary={true}
                                onClick={this.props.onModalOpen}/>;
            } else  if (this.props.form === FORM_GROUP) {

            }
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
