import React from "react";
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';


import { MDBTable, MDBTableBody, MDBTableHead } from 'mdb-react-ui-kit';

import exampleStraight from '../assets/straight_param.png';
import exampleT from '../assets/t_param.png';
import exampleCross from '../assets/cross_param.png';


class FlowPresentation extends React.Component {
    renderTable(types, directions, layers = 2) {
        var table = []
        var t, src, d
        
        try {
            if (layers == 1) {
                for (t in types) for (src in directions) {
                    console.log(src, directions[src])
                    console.log(t, types[t])
                    console.log(this.props.flow[t][src])

                    table.push(<tr>
                        <td scope='col'>{ directions[src] }</td>
                        <td scope='col'>{ types[t] }</td>
                        <td scope='col'>{ this.props.flow[t][src] }</td>
                    </tr>)
                }
            }
            if (layers == 2) {
                for (t in types) for (src in directions) for (d in directions[src]) {
                    table.push(<tr>
                        <td scope='col'>{ directions[src][d] }</td>
                        <td scope='col'>{ types[t] }</td>
                        <td scope='col'>{ this.props.flow[t][src][d] }</td>
                    </tr>)
                }
            }
        } catch (error) {
            console.log(error)
        }
        return table
    }

    renderStraight() {
        var types = {
            // 'person': '行人',
            'bicycle': '腳踏車',
            'car': '小客車',
            'motorbike': '機車',
            'large': '大車'
        }, directions = {
            "Forward": '實線往虛線車流',
            "Reverse": '虛線往實線車流'
        }
        return (
            <Container>
                <Row><Col><h3>路段俯視圖</h3></Col></Row>
                <Row><Col style={{ textAlign: 'center' }}><img style={{ width: '100%' }} src={exampleStraight} /></Col></Row>
                <Row><Col>
                    <MDBTable striped hover>
                        <MDBTableHead>
                            <tr>
                                <th scope='col'>流量種類</th>
                                <th scope='col'>車種</th>
                                <th scope='col'>流量計數</th>
                            </tr>
                        </MDBTableHead>
                        <MDBTableBody> {this.renderTable(types, directions, 1)} </MDBTableBody>
                    </MDBTable>
                </Col></Row>
            </Container>
        )
    }

    renderT() {
        var types = {
            // 'person': '行人',
            'bicycle': '腳踏車',
            'car': '小客車',
            'motorbike': '機車',
            'large': '大車'
        }, directions = {
            "A": {
                "Left": '來自 A 的左轉車流',
                "Straight": '來自 A 的直走車流'
            },
            "B": {
                "Right": '來自 B 的右轉車流',
                "Straight": '來自 B 的直走車流'
            },
            "T": {
                "Left": '來自 T 的左轉車流',
                "Right": '來自 T 的右轉車流',
            }
        }
        return (
            <Container>
                <Row><Col><h3>T 字路口俯視圖</h3></Col></Row>
                <Row><Col style={{ textAlign: 'center' }}><img style={{ width: '100%' }} src={exampleT} /></Col></Row>
                <Row><Col>
                    <MDBTable striped hover>
                        <MDBTableHead>
                            <tr>
                                <th scope='col'>流量種類</th>
                                <th scope='col'>車種</th>
                                <th scope='col'>流量計數</th>
                            </tr>
                        </MDBTableHead>
                        <MDBTableBody> {this.renderTable(types, directions)} </MDBTableBody>
                    </MDBTable>
                </Col></Row>
            </Container>
        )
    }

    renderCross() {
        var types = {
            // 'person': '行人',
            'bicycle': '腳踏車',
            'car': '小客車',
            'motorbike': '機車',
            'large': '大車'
        }, directions = {
            "A": {
                "Left": '來自 A 的左轉車流',
                "Right": '來自 A 的右轉車流',
                "Straight": '來自 A 的直走車流'
            },
            "B": {
                "Left": '來自 B 的左轉車流',
                "Right": '來自 B 的右轉車流',
                "Straight": '來自 B 的直走車流'
            },
            "X": {
                "Left": '來自 X 的左轉車流',
                "Right": '來自 X 的右轉車流',
                "Straight": '來自 X 的直走車流'
            },
            "Y": {
                "Left": '來自 Y 的左轉車流',
                "Right": '來自 Y 的右轉車流',
                "Straight": '來自 Y 的直走車流'
            }
        }
        return (
            <Container>
                <Row><Col><h3>十字路口俯視圖</h3></Col></Row>
                <Row><Col style={{ textAlign: 'center' }}><img style={{ width: '100%' }} src={exampleCross} /></Col></Row>
                <Row><Col>
                    <MDBTable striped hover>
                        <MDBTableHead>
                            <tr>
                                <th scope='col'>流量種類</th>
                                <th scope='col'>車種</th>
                                <th scope='col'>流量計數</th>
                            </tr>
                        </MDBTableHead>
                        <MDBTableBody> {this.renderTable(types, directions)} </MDBTableBody>
                    </MDBTable>
                </Col></Row>
            </Container>
        )
    }

    render() {
        if (this.props.mode == "straight") {
            return this.renderStraight()
        }
        if (this.props.mode == "t_intersection") {
            return this.renderT()
        }
        if (this.props.mode == "cross_intersection") {
            return this.renderCross()
        }
    }
}

FlowPresentation.propTypes = {
    mode: PropTypes.string,
    flow: PropTypes.object
};

export default FlowPresentation;