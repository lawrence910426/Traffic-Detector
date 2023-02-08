import React from 'react';
import PropTypes from 'prop-types';

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
          (<Progress reset={this.props.reset} complete={this.computationComplete.bind(this)} video={this.props.video} />) : 
          (<Data reset={this.props.reset} video={this.props.video} mode={this.props.mode} />)
        }
      </div>
    )
  }
}

Results.propTypes = {
  reset: PropTypes.func,
  video: PropTypes.string,
  mode: PropTypes.string
};


export default Results;
