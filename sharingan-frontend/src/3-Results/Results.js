import React from 'react';

import Data from './Data';
import Progress from './Progress';

class Results extends React.Component {
  constructor() {
    super();
    this.state = {
      isLoading: true
    };
  }

  computationComplete() {
    this.setState({ isLoading: false });
  }

  render() {
    return (
      <div>
        {
          this.state.isLoading ? 
          (<Progress reset={this.props.reset} complete={this.computationComplete.bind(this)} />) : 
          (<Data reset={this.props.reset} />)
        }
      </div>
    )
  }
}

export default Results;
