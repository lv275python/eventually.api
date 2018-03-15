import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import SvgIcon from 'material-ui/SvgIcon';
import ModeEdit from 'material-ui/svg-icons/editor/mode-edit';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import { putEditItemService } from 'src/containers';


export default class EditTopicDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            name: props.name,
            description: props.description,
            form: props.form,
            messageName: '',
            nameIsValid: true,
            messageDescription: '',
            descriptionIsValid: true
        };
    }

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({
            open: false,
            messageName: '',
            nameIsValid: true,
            messageDescription: '',
            descriptionIsValid: true
        });
    };

    handleName = event => {
        const regex = /^.{4,255}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                messageName: '',
                name: event.target.value,
                nameIsValid: true,
            });
        } else {
            this.setState({
                messageName: 'Required a minimum length of 4 characters',
                nameIsValid: false,
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

    handleChange = (event, index, value) => this.setState({'form': value});

    handleSubmit = () => {
        if(this.state.nameIsValid & this.state.descriptionIsValid){
            const data = {
                'name': this.state.name,
                'description': this.state.description,
                'form': this.state.form
            };
            putEditItemService(
                this.props.curriculumId, this.props.topicId, this.props.id, data
            ).then(response => {
                this.props.getItemList();
                this.handleClose();
            });

        }
    };

    render() {
        const disable = !(this.state.nameIsValid && this.state.descriptionIsValid);
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
                    onClick={this.handleOpen} />
                <Dialog
                    title="Edit item"
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                >
                    <TextField
                        floatingLabelText="Name"
                        defaultValue={this.state.name}
                        fullWidth={true}
                        onChange={this.handleName}
                        errorText={this.state.messageName} />
                    <TextField
                        floatingLabelText="Description"
                        defaultValue={this.state.description}
                        onChange={this.handleDescription}
                        errorText={this.state.messageDescription}
                        multiLine={true}
                        rowsMax={4}
                        fullWidth={true} />
                    <SelectField
                        floatingLabelText="Select form"
                        value={this.state.form}
                        onChange={this.handleChange}>
                        <MenuItem value={0} primaryText="Theoretic" />
                        <MenuItem value={1} primaryText="Practice" />
                        <MenuItem value={2} primaryText="Group" />
                    </SelectField>
                </Dialog>
            </div>
        );
    }
}
