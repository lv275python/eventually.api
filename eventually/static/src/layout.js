import React from "react";

import MainRoute from './router';
import Header from './components/header/header';

export default class Layout extends React.Component {
    render() {
        return (
            <div>
                <Header />
                <MainRoute />
            </div>
        )
    }
};

