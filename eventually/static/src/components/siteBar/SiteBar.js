import React from 'react';
import Drawer from 'material-ui/Drawer';
import SiteBarItem from './SiteBarItem';
import {withRouter} from 'react-router-dom';
import {getUserId} from 'src/helper';


class SiteBar extends React.Component {

    constructor(props) {
        super(props);
    }

    goToHome = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/home');
    };

    goToProfile = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/profile/' + getUserId());
    };

    goToProgress = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/progress');
    };

    goToCurriculum = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/curriculums');
    };

    goToDashboard = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/dashboard');
    };

    goToEvents = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/events');
    };

    goToSuggestedTopics = () => {
        this.props.toggleSiteBarOpen();
        this.props.history.push('/suggestedtopics');
    };

    render() {
        return (
            <div>
                <Drawer open={this.props.open}
                    docked={false}
                    onRequestChange={this.props.toggleSiteBarOpen}>
                    <SiteBarItem itemName={'Home'} itemClick={this.goToHome} />
                    <SiteBarItem itemName={'Profile'} itemClick={this.goToProfile} />
                    <SiteBarItem itemName={'Dashboard'} itemClick={this.goToDashboard} />
                    <SiteBarItem itemName={'My progress'} itemClick={this.goToProgress} />
                    <SiteBarItem itemName={'Curriculums'} itemClick={this.goToCurriculum} />
                    <SiteBarItem itemName={'Events'} itemClick={this.goToEvents} />
                    <SiteBarItem itemName={'Suggested Topics'} itemClick={this.goToSuggestedTopics} />
                </Drawer>
            </div>
        );
    }
}

export default withRouter(SiteBar);
