import React from 'react';

const homeImage = {
    backgroundImage: 'url(https://media.boingboing.net/wp-content/uploads/2015/05/lean.jpg)',
    height: '90vh',
    backgroundSize: 'cover'
};

export default class Home extends React.Component {
    render() {
        return (
            <div style={homeImage}>
            </div>
        );
    }
}
