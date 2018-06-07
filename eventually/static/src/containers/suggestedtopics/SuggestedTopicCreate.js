import React from 'react';
import AutoComplete from 'material-ui/AutoComplete';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import TextField from 'material-ui/TextField';
import ContentAdd from 'material-ui/svg-icons/content/add';
import {postSuggestedTopicsItem, getTopicAllTitleService} from './SuggestedTopicsService';

const FlatButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

const SuggestedTopicCreateDialogStyle = {
    zIndex: 800
};

export default class SuggestedTopicCreate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            validationField: {
                failNameMessage: '',
                failDescriptionMessage: '',
                nameIsValid: false,
                descriptionIsValid: false
            },
            open: false,
            name: '',
            dataSource:[],
            description: '',
        };
    }

    componentWillMount() {
        this.getData();
    }

    getData = () => {
        getTopicAllTitleService().then(response => {
            this.setState({
                'dataSource': response.data['topics_name']
            });
        });
    }

    handleUpdateInput = (value) => {
        const regex = /^[\S\s].{4,64}$/;
        if(regex.test(value) === true ) {
            this.setState({
                failNameMessage: '',
                nameIsValid: true,
                name: value,
            });
        } else {
            this.setState({
                failNameMessage: 'Invalid name',
                nameIsValid: false
            });
        }
    };

    handleChangeDescription = event => {
        const regex = /^[\S\s].{10,1024}$/;
        if(regex.test(event.target.value) === true ) {
            this.setState({
                failDescriptionMessage: '',
                descriptionIsValid: true,
                description: event.target.value
            });
        } else {
            this.setState({
                failDescriptionMessage: 'Invalid description',
                descriptionIsValid: false
            });
        }
    };

    handleSubmit = event => {
        if(this.state.descriptionIsValid === true && this.state.nameIsValid === true){
            const data = {
                'name': this.state.name,
                'description': this.state.description
            };
            postSuggestedTopicsItem(data).then(response => {
                this.props.getSuggestedTopicsItem();
                this.handleClose();
            });
        }
    };

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({ open: false });
        this.setState({
            name: '',
            description: ''
        });
    };

    render() {
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
                disabled={this.state.descriptionIsValid === true & this.state.nameIsValid === true ? false : true}
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
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                    style={SuggestedTopicCreateDialogStyle}>
                    <AutoComplete
                        listStyle={{ maxHeight: 200, overflow: 'auto',}}
                        hintText="minimum 4 characters"
                        floatingLabelText="Enter name of topic that you suggest"
                        fullWidth={true}
                        errorText={this.state.failNameMessage}
                        filter={AutoComplete.caseInsensitiveFilter}
                        dataSource = {this.state.dataSource}
                        onUpdateInput={this.handleUpdateInput}
                    />
                    <TextField
                        hintText="minimum 10 characters"
                        floatingLabelText="Enter description of topic you suggest"
                        defaultValue={this.state.description}
                        fullWidth={true}
                        multiLine={true}
                        rowsMax={4}
                        errorText={this.state.failDescriptionMessage}
                        onChange={this.handleChangeDescription}/>
                </Dialog>
            </div>
        );
    }
}

