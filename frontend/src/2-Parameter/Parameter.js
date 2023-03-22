import * as React from 'react';
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import PeriodSelection from "./PeriodSelection";
import ImageEditor from "./ImageEditor";
import UserHint from "./UserHint"

import { MDBBtn } from 'mdb-react-ui-kit';
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
      detector: {},
      stabilization: 10,
      id: props.video,
      modeValue: '0'
    }
    this.modeMapping = [ "straight", "t_intersection", "cross_intersection" ]
  }

  updateDetector(detectorInfo) {
    this.setState({ detector: detectorInfo })
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
    return (
      <div>
        <Container>
          <Row><Col>
            <PeriodSelection period={this.updateStabilization.bind(this)} />
          </Col></Row>

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

          <Row style={{ marginTop: '3rem' }}><Col>
            <h5>以指令執行模型</h5>
          </Col><Col><h5>
            { `python rpc_terminal.py videos/${this.props.video} --mode ${this.modeMapping[this.state.modeValue]} 
              --detector_line_t ${this.detector["T"]["x1"]},${this.detector["T"]["y1"]},${this.detector["T"]["x2"]},${this.detector["T"]["y2"]}
              --detector_line_a ${this.detector["A"]["x1"]},${this.detector["A"]["y1"]},${this.detector["A"]["x2"]},${this.detector["A"]["y2"]}
              --detector_line_b ${this.detector["B"]["x1"]},${this.detector["B"]["y1"]},${this.detector["B"]["x2"]},${this.detector["B"]["y2"]}
              --detector_line_x ${this.detector["X"]["x1"]},${this.detector["X"]["y1"]},${this.detector["X"]["x2"]},${this.detector["X"]["y2"]}
              --detector_line_y ${this.detector["Y"]["x1"]},${this.detector["Y"]["y1"]},${this.detector["Y"]["x2"]},${this.detector["Y"]["y2"]}` }
          </h5></Col></Row>
          
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