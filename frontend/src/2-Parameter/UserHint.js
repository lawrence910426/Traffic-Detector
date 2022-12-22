import React from "react";
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import exampleStraight from '../assets/logo-tw.png';
import paramStraight from '../assets/logo-tw.png';

import exampleT from '../assets/logo-tw.png';
import paramT from '../assets/logo-tw.png';

import exampleCross from '../assets/logo-tw.png';
import paramCross from '../assets/logo-tw.png';


class UserHint extends React.Component {
    renderStraight() {
        return (
            <Container><Row>
                <Col>
                    <Row><Col><h3>路段俯視圖</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}><img src={exampleStraight} /></Col></Row>
                </Col>
                <Col>
                    <Row><Col><h3>路段偵測線範例</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}><img src={paramStraight} /></Col></Row>
                </Col>
            </Row></Container>
        )
    }

    renderT() {
        return (
            <Container><Row>
                <Col>
                    <Row><Col><h3>T 字路口俯視圖</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}><img src={exampleT} /></Col></Row>
                </Col>
                <Col>
                    <Row><Col><h3>T 字路口偵測線範例</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}><img src={paramT} /></Col></Row>
                </Col>
            </Row></Container>
        )
    }

    renderCross() {
        return (
            <Container><Row>
                <Col>
                    <Row><Col><h3>十字路口俯視圖</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}><img src={exampleCross} /></Col></Row>
                </Col>
                <Col>
                    <Row><Col><h3>十字路口偵測線範例</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}><img src={paramCross} /></Col></Row>
                </Col>
            </Row></Container>
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

UserHint.propTypes = {
    mode: PropTypes.string
};

export default UserHint;