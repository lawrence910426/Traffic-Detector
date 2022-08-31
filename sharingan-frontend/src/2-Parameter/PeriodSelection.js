import React from "react";

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { MDBCard, MDBCardBody, MDBCardTitle } from 'mdb-react-ui-kit';
import Slider from '@mui/material/Slider';

class PeriodSelection extends React.Component {
  constructor() {
    super();
    this.marks = [
      {
        value: 0,
        label: '0 (sec)',
      },
      {
        value: 30,
        label: '20 (sec)',
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
      <MDBCard>
        <MDBCardBody>
          <MDBCardTitle>選擇穩定週期</MDBCardTitle>
          <Container>
            <Row><Col>
              <Slider
                aria-label="Restricted values"
                defaultValue={10}
                max={90}
                valueLabelFormat={this.valueLabelFormat}
                getAriaValueText={this.valuetext}
                step={1}
                valueLabelDisplay="on"
                marks={this.marks}
              />
            </Col></Row>
          </Container>
        </MDBCardBody>
      </MDBCard>
    );
  }
}

export default PeriodSelection;