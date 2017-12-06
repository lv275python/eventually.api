import React from "react";
import AppBar from 'material-ui/AppBar';
import Logout from '../../containers/register_login/logout.js';

export default class Header extends React.Component {
    constructor(props){
        super(props);
    }
    render() {
        return (
            <div>
              <AppBar
          title="Title"
          iconElementRight={<Logout />}
        />
            </div>
        )
    }
}
