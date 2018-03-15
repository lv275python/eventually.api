import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import SvgIcon from 'material-ui/SvgIcon';
import ModeEdit from 'material-ui/svg-icons/editor/mode-edit';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import { putEditTopicService } from 'src/containers';


export default class EditTopicDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            title: props.topicDetail['title'],
            description: props.topicDetail['description'],
            topicId: props.topicId,
            curriculumId: props.curriculumId,
            messageTitle: '',
            titleIsValid: false,
            messageDescription: '',
            descriptionIsValid: false
        };
    }

    componentWillReceiveProps(nextProps){
        if(this.props.topicDetail !== nextProps.topicDetail){
            this.setState({
                title: nextProps.topicDetail['title'],
                description: nextProps.topicDetail['description']
            });
        }
    }

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({
            open: false,
            messageTitle: '',
            titleIsValid: false,

        });
    };

    handleTitle = event => {
        const regex = /^.{4,255}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                messageTitle: '',
                title: event.target.value,
                titleIsValid: true,
            });
        } else {
            this.setState({
                messageTitle: 'Required a minimum length of 4 characters',
                titleIsValid: false,
            });
        }
    };

    handleDescription = event => {
        const regex = /^.{10,1024}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                messageDescription: '',
                description: event.target.value,
                descriptionIsValid: true,
            });
        } else {
            this.setState({
                messageDescription: 'Required a minimum length of 10 characters, maximum length of 1024 characters',
                descriptionIsValid: false,
            });
        }
    };

    handleSubmit = () => {
        if(this.state.titleIsValid === true){
            const data = {
                'title': this.state.title,
                'description': this.state.description
            };
            putEditTopicService(this.state.curriculumId, this.state.topicId, data).then(response => {
                this.props.getTopicData();
                this.handleClose();
            });
        }
    };

    render() {
        const disable = !(this.state.titleIsValid & this.state.descriptionIsValid);
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                onClick={this.handleSubmit}
                disabled={disable}
            />,
        ];
        return (
            <div>
                <RaisedButton
                    icon={<ModeEdit />}
                    label='Edit topic'
                    onClick={this.handleOpen} />
                <Dialog
                    title="Edit topic"
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                >
                    <TextField
                        floatingLabelText="Title"
                        defaultValue={this.state.title}
                        fullWidth={true}
                        onChange={this.handleTitle}
                        errorText={this.state.messageTitle} />
                    <TextField
                        floatingLabelText="Description"
                        defaultValue={this.state.description}
                        onChange={this.handleDescription}
                        multiLine={true}
                        rowsMax={4}
                        fullWidth={true} />
                </Dialog>
            </div>
        );
    }
}
