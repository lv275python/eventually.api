import React from "react";
import ItemsList from './ItemsList';
import MessagesBar from './MessagesBar';
import ProgressGraph from "./ProgressGraph";
import {itemsListService} from './profileService';

const profileStyle = {
    display: 'flex',
    justifyContent: 'space-between'
};

const itemsListStyle = {
    'width': '25%'
};

const progressGraphStyle = {
    'width': '55%',
    'margin': 2.5
};

const messagesBarStyle = {
    'width': '30%'
};

export default class Profile extends React.Component {

    constructor(props) {
        super(props);
        this.state = {}
    }

    componentWillMount() {
        this.setState({items: itemsListService().items})
    }

    render() {
        return (
            <div style={profileStyle}>
                <ItemsList items={this.state.items} style={itemsListStyle}/>
                <ProgressGraph style={progressGraphStyle}/>
                <MessagesBar style={messagesBarStyle} />
            </div>
        );
    }
}
