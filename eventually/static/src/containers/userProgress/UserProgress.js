import React from 'react';
import {ItemsList, MessagesBar, ProgressGraph} from './containers';

const userProgressStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'stretch'
};

const itemsGraphWrapperStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '70%'
};

const itemsGraphStyle = {
    paddingTop: 10,
    width: '90%',
    maxWidth: '90%'
};

const messagesBarStyle = {
    width: '30%',
    position: 'relative'
};

export default class ProgressProfile extends React.Component {

    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div style={userProgressStyle}>
                <div style={itemsGraphWrapperStyle}>
                    <ItemsList items={this.state.items} style={itemsGraphStyle}/>
                    <ProgressGraph style={itemsGraphStyle}/>
                </div>
                <MessagesBar 
                    style={messagesBarStyle} 
                    location={this.props.location.pathname.slice(1)} 
                    expandedWidth={'30%'}
                    wrappedWidth={'5%'}
                    type='student'
                />
            </div>
        );
    }
}
