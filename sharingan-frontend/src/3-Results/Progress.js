import React from 'react';
import PropTypes from 'prop-types';

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';

import { MDBBtn } from 'mdb-react-ui-kit';

import axios from 'axios'
import config from '../utils/config'

class Progress extends React.Component {
  constructor() {
    super();
    this.state = {
      progress: 0
    };
  }

  componentDidMount() {
    this.intervalId = setInterval(async () => {
        await axios.get(config.host + "progress", {
            params: { taskId: this.props.task }
        })
    }, 1000)
  }

  terminateCompute() {
    this.props.reset(); 
  }

  render() {
    return (
        <Container>
            <Row><Col>
                <h3 style={{ textAlign: 'center' }}>
                    請稍候，伺服器正在計算交通流量
                </h3>
                <label style={{ textAlign: 'center', width: '100%' }}>
                    預計剩餘時間：3 小時 15 分鐘
                </label>
            </Col></Row>

            <Row style={{ marginTop: '1rem' }}><Col>
                <div className="progress" style={{height: '20px'}}>
                <div className="progress-bar" 
                    role="progressbar" 
                    style={{width: this.state.progress + '%'}} 
                    aria-valuenow={this.state.progress} 
                    aria-valuemin="0" aria-valuemax="100">
                    {this.state.progress}%
                </div>
                </div>
            </Col></Row>

            <Row style={{ marginTop: '1rem' }}><Col>
                <MDBBtn color='danger' onClick={this.terminateCompute.bind(this)}>
                    終止計算，重新上傳影片
                </MDBBtn>
            </Col></Row>
        </Container>
    )
  }
}

Progress.propTypes = {
    complete: PropTypes.func,
    reset: PropTypes.func,
    task: PropTypes.string
};

export default Progress;
