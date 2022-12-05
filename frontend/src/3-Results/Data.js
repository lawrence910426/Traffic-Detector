import React from 'react';
import PropTypes from 'prop-types';

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import { MDBBtn, MDBTable, MDBTableBody, MDBTableHead } from 'mdb-react-ui-kit';

import { utils, writeFile } from 'xlsx';
import axios from 'axios'
import config from '../utils/config'

class Data extends React.Component {
    constructor() {
        super()
        this.state = { 
            sheet: utils.json_to_sheet([
                { 車種: '小客車', 順向流量: 0, 逆向流量: 0 },
                { 車種: '機車', 順向流量: 0, 逆向流量: 0 },
                { 車種: '大車', 順向流量: 0, 逆向流量: 0 },
                { 車種: 'MCU', 順向流量: 0, 逆向流量: 0 }
                ], { header: ["車種", "順向流量", "逆向流量"] }
            ),
            flow: {
                car: { Forward: 0, Reverse: 0 },
                motorbike: { Forward: 0, Reverse: 0 },
                large: { Forward: 0, Reverse: 0 },
                mcu: { Forward: 0, Reverse: 0 }
            },
            videoUrl: "http://techslides.com/demos/sample-videos/small.mp4"
        }
    }

    async componentDidMount() {
        var flow = await axios.get(config.host + "flow", {
            params: { taskId: this.props.task, videoId: this.props.video }
        })
        flow = flow.data
        
        flow.large = {}
        flow.large.Forward = flow.truck.Forward + flow.bus.Forward
        flow.large.Reverse = flow.truck.Reverse + flow.bus.Reverse

        flow.mcu = {}
        flow.mcu.Forward = 0
        flow.mcu.Reverse = 0
        this.setState({ flow: flow })
        
        var worksheet = utils.json_to_sheet([
            { 車種: '小客車', 順向流量: flow.car.Forward, 逆向流量: flow.car.Reverse },
            { 車種: '機車', 順向流量: flow.motorbike.Forward, 逆向流量: flow.motorbike.Reverse },
            { 車種: '大車', 順向流量: flow.large.Forward, 逆向流量: flow.large.Reverse },
            { 車種: 'MCU', 順向流量: flow.mcu.Forward, 逆向流量: flow.mcu.Reverse }
            ], { header: ["車種", "順向流量", "逆向流量"] }
        )
        this.setState({ sheet: worksheet })
        
        this.setState({ videoUrl: flow.videoUrl })
    }
   
    downloadVideo() {
        window.open(this.state.videoUrl)
    }
    
    downloadExcel() {
        const workbook = utils.book_new();
        utils.book_append_sheet(workbook, this.state.sheet, "交通流量計數");
        writeFile(workbook, "Traffic.xlsb")
    }

    downloadVideo() {
        window.open(this.state.videoUrl)
    }

    render() {
        return (
            <Container>
                <Row>
                    <Col style={{ marginTop: '1rem' }}>
                        <MDBTable striped hover>
                            <MDBTableHead>
                                <tr>
                                    <th scope='col'>車種</th>
                                    <th scope='col'>順向流量</th>
                                    <th scope='col'>反向流量</th>
                                </tr>
                            </MDBTableHead>
                            <MDBTableBody>
                                <tr>
                                    <th scope='row'>小客車</th>
                                    <td>{this.state.flow.car.Forward}</td>
                                    <td>{this.state.flow.car.Reverse}</td>
                                </tr>
                                <tr>
                                    <th scope='row'>機車</th>
                                    <td>{this.state.flow.motorbike.Forward}</td>
                                    <td>{this.state.flow.motorbike.Reverse}</td>
                                </tr>
                                <tr>
                                    <th scope='row'>大車</th>
                                    <td>{this.state.flow.large.Forward}</td>
                                    <td>{this.state.flow.large.Reverse}</td>
                                </tr>
                                <tr>
                                    <th scope='row'>MCU</th>
                                    <td>{this.state.flow.mcu.Forward}</td>
                                    <td>{this.state.flow.mcu.Reverse}</td>
                                </tr>
                            </MDBTableBody>

                        </MDBTable>
                        <MDBBtn onClick={this.downloadExcel}>下載交通流量結果</MDBBtn>
                    </Col>

                    <Col style={{ marginTop: '1rem' }}>
                        <video src={this.state.videoUrl} width="100%" controls autoPlay>
                            <source src={this.state.videoUrl} type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                        <MDBBtn onClick={this.downloadVideo.bind(this)}>下載影片</MDBBtn>
                    </Col>
                </Row>

                <Row style={{ marginTop: '1rem' }}>
                    <Col><MDBBtn onClick={this.props.reset}>完成分析，回到上傳影片頁面</MDBBtn></Col>
                </Row>
            </Container>
        )
    }
}

Data.propTypes = {
    reset: PropTypes.func,
    task: PropTypes.string,
    video: PropTypes.string
};

export default Data;
