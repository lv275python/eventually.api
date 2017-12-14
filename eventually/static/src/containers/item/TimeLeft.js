import React from 'react';
import Countdown from 'react-countdown-now';

class TimeLeft extends React.Component {
    render(){
        return(
            <div>
                <h2>Timeleft</h2>
                <Countdown date={Date.now() + this.props.time} /> 
            </div>
        );
    }
}
export default TimeLeft;
