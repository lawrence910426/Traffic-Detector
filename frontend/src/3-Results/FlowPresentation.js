import React from "react";
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';


import { MDBTable, MDBTableBody, MDBTableHead } from 'mdb-react-ui-kit';

import exampleStraight from '../assets/logo-tw.png';
import exampleT from '../assets/logo-tw.png';
import exampleCross from '../assets/logo-tw.png';


class FlowPresentation extends React.Component {
    renderStraight() {
        return (
            <Container>
                <Row><Col><h3>路段俯視圖</h3></Col></Row>
                <Row><Col style={{ textAlign: 'center' }}><img src={exampleStraight} /></Col></Row>
                <Row><Col>
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
                                <th scope='row'>行人</th>
                                <td>{this.props.flow.pedestrian.Forward}</td>
                                <td>{this.props.flow.pedestrian.Reverse}</td>
                            </tr>
                            <tr>
                                <th scope='row'>腳踏車</th>
                                <td>{this.props.flow.bicycle.Forward}</td>
                                <td>{this.props.flow.bicycle.Reverse}</td>
                            </tr>
                            <tr>
                                <th scope='row'>小客車</th>
                                <td>{this.props.flow.car.Forward}</td>
                                <td>{this.props.flow.car.Reverse}</td>
                            </tr>
                            <tr>
                                <th scope='row'>機車</th>
                                <td>{this.props.flow.motorbike.Forward}</td>
                                <td>{this.props.flow.motorbike.Reverse}</td>
                            </tr>
                            <tr>
                                <th scope='row'>大車</th>
                                <td>{this.props.flow.large.Forward}</td>
                                <td>{this.props.flow.large.Reverse}</td>
                            </tr>
                        </MDBTableBody>
                    </MDBTable>
                </Col></Row>
            </Container>
        )
    }

    renderTable(types, directions) {
        var table = ""
        for (var t in types) for (var src in directions) for (var d in directions[src]) {
            table += (
                <tr>
                    <td scope='col'>{ directions[src][d] }</td>
                    <td scope='col'>{ types[t] }</td>
                    <td scope='col'>{ this.props.flow[t][src][d] }</td>
                </tr>
            )
        }
        return table
    }

    renderT() {
        var types = {
            'pedestrian': '行人',
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
                <Row><Col style={{ textAlign: 'center' }}><img src={exampleT} /></Col></Row>
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
            'pedestrian': '行人',
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
                <Row><Col style={{ textAlign: 'center' }}><img src={exampleCross} /></Col></Row>
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