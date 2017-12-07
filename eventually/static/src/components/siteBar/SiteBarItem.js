import React from 'react';
import MenuItem from 'material-ui/MenuItem';

export default class SiteBarItem extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <MenuItem onClick={this.props.itemClick}>{this.props.itemName}</MenuItem>
            </div>
        );
    }
}
