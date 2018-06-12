import React from 'react';
import Avatar from 'material-ui/Avatar';
import LibraryBooks from 'material-ui/svg-icons/av/library-books';
import Code from 'material-ui/svg-icons/action/code';
import Book from 'material-ui/svg-icons/action/book';
import FlatButton from 'material-ui/FlatButton';
import {Card, CardHeader, CardText, CardActions} from 'material-ui/Card';
import {blue500, yellow600, lime500} from 'material-ui/styles/colors';
import {putAssignmentService} from './itemsListService';
import {AssignmentUpload} from 'src/containers';


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

const STATUS_REQUESTED = 0;
const STATUS_IN_PROCESS = 1;
const STATUS_DONE = 2;

const FORM_THEORETIC = 0;
const FORM_PRACTICE = 1;
const FORM_GROUP = 2;

export default class ItemUnit extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: this.props.isActive,
            status: this.props.status
        };
    }

    handleClick = () => {
        this.props.onClick(this.props.id);
    };

    handleStartAssignment = () => {
        putAssignmentService(this.props.assignmenId, {'status': STATUS_IN_PROCESS})//.then(response => {

        // TODO then for response

    };

    componentWillReceiveProps(nextProps) {
        this.setState({
            expanded: nextProps.isActive
        });
    }

    updateStatus = status => {
        if (status === 200){
            this.setState({
                status: 2
            })
        }
    };

    render() {

        let avatar = null,
            controlButton = <FlatButton
                            label="Start assignment"
                            onClick={this.handleStartAssignment}
                            backgroundColor={lime500}/>;

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


        if (this.state.status === STATUS_IN_PROCESS) {
            if (this.props.form === FORM_THEORETIC || this.props.form === FORM_GROUP) {
                controlButton = <FlatButton
                                label="Done"
                                secondary={true}/>;

            } else if (this.props.form === FORM_PRACTICE) {
                controlButton = <AssignmentUpload
                        assignment_id={this.props.assignment_id}
                        updateStatus = {this.updateStatus}
                        />
            }

        } else if (this.state.status === STATUS_DONE){
            controlButton = <FlatButton
                            label="Completed"
                            backgroundColor={yellow600}
                            disabled={true}/>;
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
