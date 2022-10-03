import React from "react";
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import PeriodSelection from "./PeriodSelection";
import ImageEditor from "./ImageEditor";

import { MDBBtn } from 'mdb-react-ui-kit';

import axios from 'axios'
import config from '../utils/config'

class Parameters extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      detector: {
        x1: 100, y1: 100,
        x2: 200, y2: 100
      },
      stabilization: 10,
      id: props.video
    }
  }

  updateDetector(x1, y1, x2, y2) {
    // Translates Web coordinate to OpenCV coordinate
    this.setState({
      detector: {
        x1: Math.floor(y1), y1: Math.floor(x1),
        x2: Math.floor(y2), y2: Math.floor(x2)
      }
    })
  }

  updateStabilization(period) {
    this.setState({
      stabilization: period
    })
  }

  async complete() {
    var taskId = await axios.get(config.host + "task_id", {
      params: this.state
    })
    taskId = taskId.data.id
    this.props.task(taskId)
    this.props.next()
  }

  
  render() {
    return (
      <div>
        <Container>
          <Row><Col>
            <PeriodSelection period={this.updateStabilization.bind(this)} />
          </Col></Row>

          <Row style={{ marginTop: '3rem' }}><Col>
            <ImageEditor video={this.props.video} detector={this.updateDetector.bind(this)} />
          </Col></Row>

          <Row style={{ marginTop: '3rem' }}><Col>
            <MDBBtn onClick={this.complete.bind(this)}>完成參數設置</MDBBtn>
          </Col></Row>
        </Container>
      </div>
    );
  }
}

Parameters.propTypes = {
  next: PropTypes.func,
  video: PropTypes.string,
  task: PropTypes.func
};

export default Parameters;
