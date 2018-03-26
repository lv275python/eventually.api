import React, {Component} from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import {orange500} from 'material-ui/styles/colors';
import {teamServicePost, usersServiceGet} from './teamService';
import {FileUpload, CancelDialog} from 'src/containers';
import {getUserId} from 'src/helper';

const FlatButtonStyle = {
    position: 'fixed',
    right: '30%',
    top: '85%'
};

const CreateTeamDialogStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

const errorStyle = {
    color: orange500,
};

export default class CreateTeamDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            name: '',
            description: '',
            image: '',
            values: [],
            users: [],
            MessageName: '',
            MessageDescription: '',
            NameIsValid: false,
            DescriptionIsValid: true,
            openCancelDialog: false
        };
    }

    componentWillMount(){
        this.getAllUsers();
    }

    getAllUsers = () => {
        usersServiceGet().then(response => {
            this.setState({'users': response.data.users});
        });
    };

    /*set description to state after validation*/
    handleDescription = event => {
        const regex = /^[\S\s.]{0,1024}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                MessageDescription: '',
                description: event.target.value,
                DescriptionIsValid: true,
            });
        } else {
            this.setState({ MessageDescription: 'Description must contain 0-1024 symbols'});
            this.setState({ DescriptionIsValid: false});
        }
    };

    /*set name to state after validation*/
    handleName = event => {
        const regex = /^.{4,30}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                MessageName: '', 
                name: event.target.value,
                NameIsValid: true,
            });
        } else {
            this.setState({ 
                MessageName: 'Name must contain 4-30 symbols',
                NameIsValid: false,
            });
        }
    };

    /*set uploaded image to state*/
    uploadImage = imageName => {
        this.setState({image: imageName});
    };

    /*open CreateTeamDialog*/
    handleOpen = () => {
        this.setState({ open: true });
    };

    /*close CreateTeamDialog*/
    handleClose = () => {
        this.setState({ open: false });
        this.setState({
            values: [],
            name: '',
            description: '',
            image: '',
            MessageName: '',
            MessageDescription: '',
            NameIsValid: false,
            DescriptionIsValid: true,
        });
    };

    handleChange = (event, index, values) => {
        this.setState({values});
    };

    handleSubmit = () => {
        if(this.state.DescriptionIsValid === true && this.state.NameIsValid === true){
            const data = {
                'name': this.state.name,
                'description': this.state.description,
                'image': this.state.image,
                'owner': getUserId(),
                'members_id': this.state.values
            };
            teamServicePost(data).then(response => {
                this.props.getTeamItem();
                this.handleClose();
            });
        }
    };
    
    menuItems(values) {
        return this.state.users.map((user) => (
            <MenuItem
                key={user.id}
                insetChildren={true}
                checked={values && values.indexOf(user.id) > -1}
                value={user.id}
                primaryText={user.first_name + ' ' + user.last_name}
            />
        ));
    }

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
            (this.state.image != '') ||
            (this.state.users.length != 0)) {
            this.setState({openCancelDialog: true});
        }
        else this.handleClose();
    };

    render() {
        const {values} = this.state;
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleSubmit}
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
                    title={this.props.title}
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    autoDetectWindowHeight={true}
                    onRequestClose={this.handleRequestClose}
                >
                    <TextField
                        hintText="Name"
                        fullWidth={true}
                        defaultValue={this.props.title}
                        onChange={this.handleName}
                        errorText={this.state.MessageName}
                        errorStyle={errorStyle}
                    />
                    <TextField
                        defaultValue={this.props.description}
                        hintText="Description"
                        multiLine={true}
                        rowsMax={4}
                        fullWidth={true}
                        onChange={this.handleDescription}
                        errorText={this.state.MessageDescription}
                        errorStyle={errorStyle}
                    />
                    <SelectField
                        multiple={true}
                        hintText="Select members"
                        value={values}
                        onChange={this.handleChange}
                    >
                        {this.menuItems(values)}
                    </SelectField>
                    <FileUpload updateImageNameInDb={this.uploadImage}/>
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
