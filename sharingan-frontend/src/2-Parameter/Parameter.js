import React from "react";
import PropTypes from 'prop-types';

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import PeriodSelection from "./PeriodSelection";
import ImageEditor from "./ImageEditor";

import { MDBBtn } from 'mdb-react-ui-kit';

class Parameters extends React.Component {
  constructor() {
    super();
    this.marks = [
      {
        value: 0,
        label: '0 (sec)',
      },
      {
        value: 30,
        label: '30 (sec)',
      },
      {
        value: 60,
        label: '60 (sec)',
      },
      {
        value: 90,
        label: '90 (sec)',
      }
    ];
  }

  valuetext(value) { return `${value} (sec)`; }
  valueLabelFormat(value) { return `${value} (sec)`; }

  render() {
    return (
      <div>
        <Container>
          <Row><Col>
            <PeriodSelection />
          </Col></Row>

          <Row style={{ marginTop: '3rem' }}><Col>
            <ImageEditor />
          </Col></Row>

          <Row style={{ marginTop: '3rem' }}><Col>
            <MDBBtn onClick={this.props.next}>完成參數設置</MDBBtn>
          </Col></Row>
        </Container>
      </div>
    );
  }
}

Parameters.propTypes = {
  next: PropTypes.func
};

export default Parameters;