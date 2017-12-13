import React from 'react';
import ReactDOM from 'react-dom';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import {BrowserRouter as Router} from 'react-router-dom';

import Layout from './layout';

ReactDOM.render(
    <Router>
        <MuiThemeProvider>
            <Layout/>
        </MuiThemeProvider>
    </Router>,
    document.getElementById('app')
);
