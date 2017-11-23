import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router } from 'react-router-dom';

import Layout from './layout';

ReactDOM.render(
    <Router>
        <Layout />
    </Router>,
    document.getElementById('app')
);
