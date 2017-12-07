import React from 'react';
import ReactDOM from 'react-dom';
import Countdown from 'react-countdown-now';

class Timeleft extends React.Component {
    render(){
        return(
            <div>
                <h2>Timeleft</h2>
                <Countdown date={Date.now() + this.props.time} /> 
            </div>
            );
        }
}
export default Timeleft
