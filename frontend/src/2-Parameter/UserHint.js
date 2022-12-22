import React from "react";
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import exampleStraight from '../assets/straight_example.png';
import paramStraight from '../assets/straight_param.png';

import exampleT from '../assets/t_example.png';
import paramT from '../assets/t_param.png';

import exampleCross from '../assets/cross_example.png';
import paramCross from '../assets/cross_param.png';


class UserHint extends React.Component {
    renderStraight() {
        return (
            <Container><Row>
                <Col>
                    <Row><Col><h3>路段俯視圖</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}>
                        <img style={{ width: '100%' }} src={exampleStraight} />
                    </Col></Row>
                </Col>
                <Col>
                    <Row><Col><h3>路段偵測線範例</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}>
                        <img style={{ width: '100%' }} src={paramStraight} />
                    </Col></Row>
                </Col>
            </Row></Container>
        )
    }

    renderT() {
        return (
            <Container><Row>
                <Col>
                    <Row><Col><h3>T 字路口俯視圖</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}>
                        <img style={{ width: '100%' }} src={exampleT} />
                    </Col></Row>
                </Col>
                <Col>
                    <Row><Col><h3>T 字路口偵測線範例</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}>
                        <img style={{ width: '100%' }} src={paramT} />
                    </Col></Row>
                </Col>
            </Row></Container>
        )
    }

    renderCross() {
        return (
            <Container><Row>
                <Col>
                    <Row><Col><h3>十字路口俯視圖</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}>
                        <img style={{ width: '100%' }} src={exampleCross} />
                    </Col></Row>
                </Col>
                <Col>
                    <Row><Col><h3>十字路口偵測線範例</h3></Col></Row>
                    <Row><Col style={{ textAlign: 'center' }}>
                        <img style={{ width: '100%' }} src={paramCross} />
                    </Col></Row>
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