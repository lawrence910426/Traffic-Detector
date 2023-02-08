import React from 'react';
import PropTypes from 'prop-types';

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import { MDBBtn } from 'mdb-react-ui-kit';

import { utils, writeFile } from 'xlsx';
import axios from 'axios'
import config from '../utils/config'
import FlowPresentation from './FlowPresentation'

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
            flow: {},
            videoUrl: "http://techslides.com/demos/sample-videos/small.mp4"
        }
    }

    async componentDidMount() {
        var flow = await axios.get(config.host + "query_task", {
            params: { videoId: this.props.video }
        })
        flow = flow.data
        
        // Recursive addition
        const recursiveSum = (a, b) => {
            if(typeof a === 'object') {
                var ans = {}
                for (var k in a) ans[k] = recursiveSum(a[k], b[k])
            } else {
                ans = a + b
            }
            return ans
        }
        flow.large = recursiveSum(flow.truck, flow.bus)
        console.log(flow)

        this.setState({ flow: flow })
        this.setState({ videoUrl: flow.videoUrl })
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
                        <FlowPresentation mode={this.props.mode} flow={this.state.flow}></FlowPresentation>
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
    video: PropTypes.string,
    mode: PropTypes.string
};

export default Data;
