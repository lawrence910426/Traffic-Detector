import * as React from 'react';
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import PeriodSelection from "./PeriodSelection";
import ImageEditor from "./ImageEditor";
import UserHint from "./UserHint"

import { MDBBtn, MDBInput } from 'mdb-react-ui-kit';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';

import axios from 'axios'
import config from '../utils/config'

class Parameters extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      detector: {
        'X': { 'x1': 0, 'x2': 0, 'y1': 0, 'y2': 0 },
        'Y': { 'x1': 0, 'x2': 0, 'y1': 0, 'y2': 0 },
        'T': { 'x1': 0, 'x2': 0, 'y1': 0, 'y2': 0 },
        'A': { 'x1': 0, 'x2': 0, 'y1': 0, 'y2': 0 },
        'B': { 'x1': 0, 'x2': 0, 'y1': 0, 'y2': 0 },
      },
      stabilization: 10,
      slice: 1,
      id: props.video,
      modeValue: '0'
    }
    this.modeMapping = [ "straight", "t_intersection", "cross_intersection" ]
  }

  updateDetector(detectorInfo) {
    this.setState({ detector: {
      ...this.state.detector,
      ...detectorInfo 
    }})
  }

  updateStabilization(period) {
    this.setState({ stabilization: period })
  }

  async complete() {
    var params = this.state
    params.modeValue = this.modeMapping[params.modeValue]
    var result = await axios.get(config.host + "init_task", { params: params })
    var uuid = result.data.id
    console.log(uuid)

    this.props.next()
  }

  handleModeChange(event, newValue) {
    this.setState({ modeValue: newValue })
    this.props.mode(this.modeMapping[newValue])
  }

  handleSliceChange(event) {
    this.setState({ slice: event.target.value })
  }

  renderTabs(index) {
    return (
      <TabPanel value={index.toString()}>
        <Row style={{ marginTop: '3rem' }}><Col>
          <UserHint mode={this.modeMapping[index]} />
        </Col></Row>
        <Row style={{ marginTop: '3rem' }}><Col>
          <ImageEditor video={this.props.video} 
            updateDetectorCallback={this.updateDetector.bind(this)} 
            mode={this.modeMapping[index]}/>
        </Col></Row>
      </TabPanel>
    )
  }
  
  render() {
    var dtor = this.state.detector

    return (
      <div>
        <Container>
          <Row><Col>
            <PeriodSelection period={this.updateStabilization.bind(this)} />
          </Col></Row>

          <Row style={{ marginTop: '3rem' }}>
            <Col sm={4} md={2} lg={2}><h5>選擇拆分數量</h5></Col>
            <Col><MDBInput type='number' onChange={this.handleSliceChange.bind(this)} value={this.state.slice} /></Col>
          </Row>

          <Row style={{ marginTop: '3rem' }}><Col>
            <TabContext value={this.state.modeValue}>
              <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <TabList onChange={this.handleModeChange.bind(this)} aria-label="mode-selection">
                  <Tab label="路段計算" value="0" />
                  <Tab label="T 字路口" value="1" />
                  <Tab label="十字路口" value="2" />
                </TabList>
              </Box>

              {this.renderTabs(0)}
              {this.renderTabs(1)}
              {this.renderTabs(2)}
            </TabContext>
          </Col></Row>

          <Row style={{ marginTop: '3rem' }}><Col sm={4} md={2} lg={2}>
            <h5>以指令執行模型</h5>
          </Col><Col><code>
            { `python rpc_terminal.py videos/${this.props.video} --mode ${this.modeMapping[this.state.modeValue]} 
              --detector_line_t ${dtor["T"]["x1"]},${dtor["T"]["y1"]},${dtor["T"]["x2"]},${dtor["T"]["y2"]}
              --detector_line_a ${dtor["A"]["x1"]},${dtor["A"]["y1"]},${dtor["A"]["x2"]},${dtor["A"]["y2"]}
              --detector_line_b ${dtor["B"]["x1"]},${dtor["B"]["y1"]},${dtor["B"]["x2"]},${dtor["B"]["y2"]}
              --detector_line_x ${dtor["X"]["x1"]},${dtor["X"]["y1"]},${dtor["X"]["x2"]},${dtor["X"]["y2"]}
              --detector_line_y ${dtor["Y"]["x1"]},${dtor["Y"]["y1"]},${dtor["Y"]["x2"]},${dtor["Y"]["y2"]}
              --slices ${this.state.slice}` }
          </code></Col></Row>
          
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
  mode: PropTypes.func,
  video: PropTypes.string
};

export default Parameters;