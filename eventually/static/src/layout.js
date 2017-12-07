import React from "react";
import {Route, Switch} from "react-router-dom";
import MainRouter from './mainRouter';
import Header from './components/header/Header';

import { isLogged } from './utils'
import Sign from './containers/register_login/Sign'
import SignRouter from './signRouter'
import Paper from 'material-ui/Paper';
import SiteBar from './components/siteBar/SiteBar'


const style = {
  height: 300,
  width: '60%',
  margin: 'auto',
  marginLeft: '20%',
  minWidth: 300,
  position: 'relative',
  textAlign: 'center',
  display: 'inline-block',
};

export default class Layout extends React.Component {
  constructor(props) {
    super(props);
  }
    render() {
        return (
          isLogged()?
            <div>
              <Header />
                <MainRouter />
            </div>:
            <div>
              <Sign />
              <Paper style={style} zDepth={5}>
                    <SignRouter />
              </Paper>

            </div>
        )
    }
};
