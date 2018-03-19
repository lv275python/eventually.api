import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import { postItemService, CancelDialog } from 'src/containers';


const FlatButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

export default class TaskDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            name: '',
            description: '',
            form: 0,
            estimation:0,
            topicId: props.topicId,
            curriculumId: props.curriculumId,
            itemId: props.itemId,
            messageName: '',
            nameIsValid: false,
            messageDescription: '',
            descriptionIsValid: false,
            openCancelDialog: false
        };
    }

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({
            open: false,
            messageName: '',
            nameIsValid: false,
            messageDescription: '',
            descriptionIsValid: false,
            form: 0
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
        const regex = /^.{10,10000}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                messageDescription: '',
                description: event.target.value,
                descriptionIsValid: true,
            });
        } else {
            this.setState({
                messageDescription: 'Required a minimum length of 10 characters',
                descriptionIsValid: false,
            });
        }
    };

    handleChange = (event, index, value) => this.setState({'form': value});

    handleSubmit = () => {
        if(this.state.nameIsValid && this.state.descriptionIsValid){
            const data = {
                'name': this.state.name,
                'description': this.state.description,
                'form': this.state.form,
                'estimation': this.state.estimation
            };
            postItemService(this.state.curriculumId, this.state.topicId, data).then(response => {
                this.props.getItemList();
                this.handleClose();
            });
        }
    };

    handleCancelDialogClose = () => {
        this.setState({'openCancelDialog': false});
    };

    handleCancelCreateDialogClose = () => {
        this.handleCancelDialogClose();
        this.handleClose();
    };

    handleRequestClose = () => {
        if ((this.state.name != '') ||
            (this.state.description != '') ||
            (this.state.form != 0)) {
            this.setState({openCancelDialog: true});
        }
        else this.handleClose();
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
                <FloatingActionButton
                    onClick={this.handleOpen}
                    style={FlatButtonStyle}>
                    <ContentAdd />
                </FloatingActionButton>
                <Dialog
                    title="Add item"
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleRequestClose}
                >
                    <TextField
                        floatingLabelText="Name"
                        fullWidth={true}
                        onChange={this.handleName}
                        errorText={this.state.messageName} />
                    <TextField
                        floatingLabelText="Description"
                        onChange={this.handleDescription}
                        multiLine={true}
                        fullWidth={true}
                        errorText={this.state.messageDescription} />
                    <SelectField
                        floatingLabelText="Select form"
                        value={this.state.form}
                        onChange={this.handleChange}
                    >
                        <MenuItem value={0} primaryText="Theoretic" />
                        <MenuItem value={1} primaryText="Practice" />
                        <MenuItem value={2} primaryText="Group" />
                    </SelectField>
                </Dialog>
                {this.state.openCancelDialog &&
                    (<CancelDialog
                        openCancelDialog={this.state.openCancelDialog}
                        handleCancelMainDialogClose={this.handleCancelCreateDialogClose}
                        handleCancelDialogClose={this.handleCancelDialogClose}
                    />)
                }
            </div>
        );
    }
}
