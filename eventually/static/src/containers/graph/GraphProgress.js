import React from 'react';
import {AreaChart} from 'react-easy-chart';
import { getAssignments } from './graphservice';
import ToolTip from './ToolTip';

export default class GraphProgress extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            showToolTip: false,
            toolTipText: '',
            x: 0,
            y: 0,
            top: `${50}px`,
            left: `${50}px`,
            obj : [
                []
            ],
        };
    }

    componentWillMount(){
        getAssignments().then(response => {
            var tmp_obj = [[{ x: 0, y: 0 }]];
            var tmp_x = 0;
            var tmp_y = 20;
            response.data.new_date.forEach(function(item, i, arr){
                tmp_x += 10;
                if (item.statuses == 2 ){
                    tmp_y += 20;
                }
                else{
                    tmp_y -= 20;
                }
                tmp_obj[0].push({x:tmp_x, y:tmp_y, statements:item.statements});
            });
            this.setState({obj: tmp_obj});
        });
    }

  mouseOverHandler = (d, e) => {
      this.setState({
          showToolTip: true,
          top: `${e.y}px`,
          left: `${e.x}px`,
          y: d.y,
          x: d.x,
          toolTipText: d.statements,
      });
  }

  mouseMoveHandler = (e) => {
      if (this.state.showToolTip) {
          this.setState({ top: `${e.top}px`, left: `${e.left}px` });
      }
  }

  mouseOutHandler = () =>  {
      this.setState({ showToolTip: false });
  }

  createTooltip = () => {
      if (this.state.showToolTip) {
          return (
              <ToolTip
                  top={this.state.top}
                  left={this.state.left}
              >
                  {this.state.toolTipText}
              </ToolTip>
          );
      }
      return false;
  }

  render() {
      return (
          <div>
              <AreaChart
                  axes
                  dataPoints
                  grid
                  mouseOverHandler={this.mouseOverHandler}
                  mouseOutHandler={this.mouseOutHandler}
                  mouseMoveHandler={this.mouseMoveHandler}
                  areaColors={['#3E2723']}
                  width={700}
                  height={350}
                  interpolate={'cardinal'}
                  data={this.state.obj}
              />{this.createTooltip()}
          </div>
      );
  }
}
