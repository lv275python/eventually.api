import React from 'react';
import Drawer from 'material-ui/Drawer';
import SiteBarItem from "./SiteBarItem";
import {withRouter} from "react-router-dom";

class SiteBar extends React.Component {

    constructor(props) {
        super(props);
    }

    goToHome = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/home')
    };

    goToProfile = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/profile')
    };

    goToCurriculum = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/curriculum')
    };

    render() {
        return (
            <div>
                <Drawer open={this.props.open}
                        docked={false}
                        onRequestChange={this.props.toggleSiteBarOpen}>
                    <SiteBarItem itemName={'Home'} itemClick={this.goToHome} />
                    <SiteBarItem itemName={'Profile'} itemClick={this.goToProfile} />
                    <SiteBarItem itemName={'Curriculum'} itemClick={this.goToCurriculum} />
                </Drawer>
            </div>
        );
    }
}

export default withRouter(SiteBar)
