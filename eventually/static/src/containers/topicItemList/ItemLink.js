import React from 'react';
import Avatar from 'material-ui/Avatar';
import SvgIcon from 'material-ui/SvgIcon';
import ModeEdit from 'material-ui/svg-icons/editor/mode-edit';
import DeleteForever from 'material-ui/svg-icons/action/delete-forever';
import Dialog from 'material-ui/Dialog';
import LibraryBooks from 'material-ui/svg-icons/av/library-books';
import Code from 'material-ui/svg-icons/action/code';
import Group from 'material-ui/svg-icons/social/group';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import {red500} from 'material-ui/styles/colors';
import { Card, CardHeader, CardText, CardActions } from 'material-ui/Card';
import { blue500, yellow600, lime500 } from 'material-ui/styles/colors';
import { deleteItemService, EditItemDialog } from 'src/containers';


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
            expanded: this.props.isActive,
            deleteDialogOpen: false
        };
    }

    handleClick = () => {
        this.props.onClick(this.props.id);
    };

    handleDelete = () => {
        this.handleOpen();
    };

    handleOpen = () => {
        this.setState({ deleteDialogOpen: true });
    };

    handleClose = () => {
        this.setState({ deleteDialogOpen: false });
    };

    handleYes = () => {
        deleteItemService(this.props.curriculumId, this.props.topicId, this.props.id).then(response => {
            this.props.getItemList();
            this.handleClose();
        });
    };

    handleNo = () => {
        this.handleClose();
    };


    componentWillReceiveProps(nextProps) {
        this.setState({
            expanded: nextProps.isActive
        });
    }

    render() {

        let avatar = null;
        if (this.props.form === 0) {
            avatar = (<Avatar icon={<LibraryBooks />} backgroundColor={yellow600} />);
        } else if (this.props.form === 1) {
            avatar = (<Avatar icon={<Code />} backgroundColor={blue500} />);
        } else  if (this.props.form === 2) {
            avatar = (<Avatar icon={<Group />} backgroundColor={lime500} />);
        }

        let cardActions;
        if (this.props.isMentor){
            cardActions = [
                <RaisedButton
                    key={0}
                    icon={<DeleteForever color={red500} />}
                    onClick={this.handleDelete} />,
                <EditItemDialog
                    key={1}
                    topicId={this.props.topicId}
                    curriculumId={this.props.curriculumId}
                    id={this.props.id}
                    name={this.props.name}
                    description={this.props.description}
                    form={this.props.form}
                    estimation={this.props.estimation}
                    superiors={this.props.superiors}
                    items={this.props.items}
                    getItemList={this.props.getItemList} />
            ];
        }

        const actionsDialog = [
            <FlatButton
                label="Yes"
                key={1}
                primary={true}
                onClick={this.handleYes}
            />,
            <FlatButton
                label="No"
                key={0}
                primary={true}
                onClick={this.handleNo}
            />
        ];

        let estimationText;
        if (this.props.estimation){
            estimationText = 'Estimation time: ' + (this.props.estimation).toString() + ' hours';
        } else {
            estimationText = 'No estimation time';
        }
        return (
            <div>
                <Card
                    expanded={this.state.expanded}
                    onExpandChange={this.handleClick}
                >
                    <CardHeader
                        title={this.props.name}
                        subtitle={estimationText}
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
                            {cardActions}
                        </CardActions>
                    </CardText>
                    <Dialog
                        actions={actionsDialog}
                        modal={true}
                        open={this.state.deleteDialogOpen}
                    >
                        Do you really want to delete this item?
                    </Dialog>
                </Card>
            </div>
        );
    }
}
