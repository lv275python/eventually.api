import React from 'react';

const style = {
    fontSize: '20px',
    fontWeight: 'bold',
    textAlign: 'center'
};

export default class ItemsListTitle extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (<h2 style={style}>{this.props.text}</h2>);
    }
}
