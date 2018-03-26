import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import SvgIcon from 'material-ui/SvgIcon';
import ModeEdit from 'material-ui/svg-icons/editor/mode-edit';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import { putEditItemService, CancelDialog } from 'src/containers';


export default class EditTopicDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            id: props.id,
            name: props.name,
            description: props.description,
            form: props.form,
            estimation: props.estimation,
            superiorsValue: props.superiors,
            itemsList: props.items,
            messageName: '',
            nameIsValid: true,
            messageDescription: '',
            descriptionIsValid: true,
            openCancelDialog: false
        };
    }

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({
            open: false,
            name: this.props.name,
            description: this.props.description,
            form: this.props.form,
            estimation: this.props.estimation,
            superiorsValue: this.props.superiors,
            messageName: '',
            nameIsValid: true,
            messageDescription: '',
            descriptionIsValid: true,
            messageEstimation: '',
            estimationIsValid: true
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

    handleEstimation = event => {
        const regex = /^\d+$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({estimation: event.target.value});
        } else {
            this.setState({
                messageEstimation: 'Required an integer value',
                estimationIsValid: false
            });
        }
    }

    handleChange = (event, index, value) => this.setState({'form': value});

    handleSubmit = () => {
        if(this.state.nameIsValid & this.state.descriptionIsValid){
            const data = {
                'name': this.state.name,
                'description': this.state.description,
                'form': this.state.form,
                'estimation': this.state.estimation,
                'superiors': this.state.superiorsValue
            };
            putEditItemService(
                this.props.curriculumId, this.props.topicId, this.props.id, data
            ).then(response => {
                this.props.getItemList();
                this.handleClose();
            });
        }
    };

    handleCancelDialogClose = () => {
        this.setState({'openCancelDialog': false});
    };

    handleCancelEditDialogClose = () => {
        this.handleCancelDialogClose();
        this.handleClose();
    };

    handleRequestClose = () => {
        if ((this.state.name != this.props.name) ||
            (this.state.description != this.props.description) ||
            (this.state.form != this.props.form)) {
            this.setState({openCancelDialog: true});
        }
        else this.handleCancelEditDialogClose();
    };

    handleSuperiorsChange = (event, index, values) => this.setState({'superiorsValue': values});

    menuItems(values) {
        const itemId = this.props.id;
        const itemsList = this.state.itemsList.filter(function(item) {
            return !(item.id == itemId);
        });
        return itemsList.map((item) => (
            <MenuItem
                key={item.id}
                insetChildren={true}
                checked={values && this.state.superiorsValue.indexOf(item.id) > -1}
                value={item.id}
                primaryText={item.name}
            />
        ));
    }

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
                    onRequestClose={this.handleRequestClose}
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
                    <SelectField
                        floatingLabelText="Select superiors"
                        multiple={true}
                        fullWidth={true}
                        value={this.state.superiorsValue}
                        onChange={this.handleSuperiorsChange}
                    >
                        {this.menuItems(this.state.superiorsValue)}
                    </SelectField>
                    <TextField
                        floatingLabelText="Estimation (hours)"
                        onChange={this.handleEstimation}
                        fullWidth={true}
                        errorText={this.state.messageDescription} />
                </Dialog>
                {this.state.openCancelDialog &&
                    (<CancelDialog
                        openCancelDialog={this.state.openCancelDialog}
                        handleCancelMainDialogClose={this.handleCancelEditDialogClose}
                        handleCancelDialogClose={this.handleCancelDialogClose}
                    />)
                }
            </div>
        );
    }
}
