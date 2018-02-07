import React from 'react';
import AppBar from 'material-ui/AppBar';
import {Logout} from 'src/containers';
import {SiteBar} from 'src/components';

export default class Header extends React.Component {

    constructor(props){
        super(props);
        this.state = {open: false};
    }

    toggleSiteBarOpen = () => {
        this.setState({open: !this.state.open});
    };

    render() {
        return (
            <div>
                <AppBar
                    title='LearnApp'
                    iconElementRight={<Logout />}
                    onLeftIconButtonTouchTap={this.toggleSiteBarOpen}
                />
                <SiteBar
                    open={this.state.open}
                    toggleSiteBarOpen={this.toggleSiteBarOpen}/>
            </div>
        );
    }
}
