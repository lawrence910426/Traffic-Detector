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
            flow: {},
            independentFlow: {},
            videoUrl: "http://techslides.com/demos/sample-videos/small.mp4",
            result: {}
        }
    }

    async componentDidMount() {
        var result = await axios.get(config.host + "query_task", {
            params: { videoId: this.props.video }
        })
        result = result.data
        
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
        result.flow.large = recursiveSum(result.flow.truck, result.flow.bus)
        console.log(result.flow)

        this.setState({ flow: result.flow })
        this.setState({ independentFlow: result.independentFlow })
        this.setState({ videoUrl: result.videoUrl })
        this.setState({ result: result })
    }
    
    downloadExcel() {
        const workbook = utils.book_new();
        var Forward = [], Reverse = []
        for(var index in this.state.independentFlow) {
            var item = this.state.independentFlow[index]["flow"]
            console.log(item)
            Forward.push({
                "影片編號": index, 
                "汽車": item["car"]["Forward"], 
                "機車": item["motorbike"]["Forward"], 
                "大車": item["truck"]["Forward"] + item["bus"]["Forward"], 
                "腳踏車": item["bicycle"]["Forward"]
            })
            Reverse.push({
                "影片編號": index, 
                "汽車": item["car"]["Reverse"], 
                "機車": item["motorbike"]["Reverse"], 
                "大車": item["truck"]["Reverse"] + item["bus"]["Reverse"], 
                "腳踏車": item["bicycle"]["Reverse"]
            })
        }
        
        utils.book_append_sheet(workbook, 
            utils.json_to_sheet(Forward, { 
                header: ["影片編號", "汽車", "機車", "大車", "腳踏車"] 
            }), "由紅線往綠線車流"); 

        utils.book_append_sheet(workbook, 
            utils.json_to_sheet(Reverse, { 
                header: ["影片編號", "汽車", "機車", "大車", "腳踏車"] 
            }), "由綠線往紅線車流"); 

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
                        <Row><Col style={{ marginTop: '1rem' }}>
                            <FlowPresentation mode={this.props.mode} flow={this.state.flow}></FlowPresentation>
                            <MDBBtn onClick={this.downloadExcel.bind(this)}>下載交通流量結果</MDBBtn>
                        </Col></Row>

                        <Row><Col style={{ marginTop: '1rem' }}>
                            <h3>原始輸出</h3>
                            <code>{JSON.stringify(this.state.result)}</code>
                        </Col></Row>
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
