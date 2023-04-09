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
      progress: 0,
      seconds: 0,
      is_waiting: true
    };
  }

  componentDidMount() {
    var intervalId = setInterval(async () => {
      var results = await axios.get(config.host + "query_task", {
        params: { videoId: this.props.video }
      })
      if (results.data.state == "WAITING") {
        this.setState({ is_waiting: true })
        return
      }

      var progress = parseInt(results.data.progress)

      this.setState({ progress: progress })
      this.setState({ is_waiting: false })
      this.setState((prevState) => {
        return { seconds: prevState.seconds + 1 }
      })

      if (results.data.state == "COMPLETED") {
        clearInterval(intervalId)
        this.props.complete()
      }
    }, 1000)
  }

  estimateRuntime() {
    var estimateSeconds = this.state.seconds / (this.state.progress + 0.01) * 100
    console.log(this.state.seconds, this.state.progress, estimateSeconds)
    if (isNaN(estimateSeconds)) {
      return `預計剩餘時間：估計中...`
    } else {
      var secs = Math.floor(estimateSeconds % 60)
      var mins = Math.floor(estimateSeconds / 60) % 60
      var hours = Math.floor(estimateSeconds / 3600)
      return `預計剩餘時間：${hours} 小時 ${mins} 分鐘 ${secs} 秒`
    }
  }

  terminateCompute() {
    this.props.reset();
  }

  render() {
    return (
      <Container>
        <Row><Col>
          <h3 style={{ textAlign: 'center' }}>
            { this.state.is_waiting ? "正在等候其他影片執行" : "請稍候，伺服器正在計算交通流量" }
          </h3>
          <label style={{ textAlign: 'center', width: '100%' }}>
            {this.estimateRuntime()}
          </label>
        </Col></Row>

        <Row style={{ marginTop: '1rem' }}><Col>
          <div className="progress" style={{ height: '20px' }}>
            <div className="progress-bar"
              role="progressbar"
              style={{ width: this.state.progress + '%' }}
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
  video: PropTypes.string
};

export default Progress;
