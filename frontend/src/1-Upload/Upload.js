import React from 'react';
import PropTypes from 'prop-types';

import Dropzone from 'react-dropzone'
import config from '../utils/config'

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { MDBCard, MDBCardBody, MDBCardTitle } from 'mdb-react-ui-kit';
import { MDBInput, MDBBtn } from 'mdb-react-ui-kit';


Dropzone.autoDiscover = false;

class Upload extends React.Component {
  constructor() {
    super();
    this.state = { progress: 0 };
  }

  change(event) {
    this.props.video(event.target.value);
  }

  complete() {
    this.props.next();
  }

  render() {
    return (
      <div>
        <Container>
          <Row><Col>
            <MDBCard>
              <MDBCardBody>
                <MDBCardTitle>輸入影片路徑</MDBCardTitle>
                <Container>
                  <Row>
                    <Col>
                      <MDBInput label='Video Path' id='path' type='text' onChange={this.change.bind(this)} />
                    </Col>
                  </Row>
                </Container>
              </MDBCardBody>
            </MDBCard>
          </Col></Row>
          
          <Row style={{ marginTop: '3rem' }}><Col>
            <MDBBtn onClick={this.complete.bind(this)}>下一步</MDBBtn>
          </Col><Col>
            <MDBBtn onClick={window.open(config.nextcloud)}>開啟 NextCloud</MDBBtn>
          </Col></Row>
        </Container>
      </div>
    );
  }
}

Upload.propTypes = {
  next: PropTypes.func,
  video: PropTypes.func
};

export default Upload;
