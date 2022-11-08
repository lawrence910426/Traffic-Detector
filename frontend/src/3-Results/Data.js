import React from 'react';
import PropTypes from 'prop-types';

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

import { MDBBtn, MDBTable, MDBTableBody, MDBTableHead, MDBInput } from 'mdb-react-ui-kit';

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
            video: {
                authState: 'unauthorized',
                authToken: undefined,
                url: undefined
            }
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
    }

    authcodeChanged(e) { this.setState({ video: { authToken: e.target.value } }) }

    downloadExcel() {
        const workbook = utils.book_new();
        utils.book_append_sheet(workbook, this.state.sheet, "交通流量計數");
        writeFile(workbook, "Traffic.xlsb")
    }

    authenticateVideo() {
        this.setState({ video: { authState: 'authorizing' } })
    }

    retrieveVideo() {
        this.setState({ video: { authState: 'authorized' } })
    }

    videoComponent() {
        if (this.state.video.authState == 'authorized') {
            return (
                <iframe
                    width="560"
                    height="315"
                    src={this.state.video.url}
                    title="YouTube video player"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
                </iframe>
            )
        } else {
            return (<h3>請點擊上方按鈕以查看影片</h3>)
        }
    }

    render() {
        return (
            <Container>
                <Modal show={this.state.video.authState == 'authroizing'} onHide={this.retrieveVideo.bind(this)}>
                    <Modal.Header closeButton>
                        <Modal.Title>請輸入授權碼</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <MDBInput onChange={this.authcodeChanged.bind(this)} type='text' />
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="primary" onClick={this.retrieveVideo.bind(this)}>
                            確認送出
                        </Button>
                    </Modal.Footer>
                </Modal>

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
                        <MDBBtn onClick={this.downloadExcel.bind(this)}>下載 Excel 交通流量結果</MDBBtn>
                    </Col>

                    <Col style={{ marginTop: '1rem' }}>
                        <MDBBtn>查看影片</MDBBtn>
                        {this.videoComponent()}
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
