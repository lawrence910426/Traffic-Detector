import React, { useState, useEffect, useRef } from "react";
import TuiImageEditor from "tui-image-editor";

import "tui-image-editor/dist/tui-image-editor.css";
import "tui-color-picker/dist/tui-color-picker.css";

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBCardLink } from 'mdb-react-ui-kit';

class ImageEditor extends React.Component {
  rootEl = React.createRef();
  imageEditorInst = null;

  componentDidMount() {
    this.imageEditorInst = new TuiImageEditor(this.rootEl.current, {
      includeUI: {
        menu: ["icon"],
        initMenu: "icon",
        uiSize: {
          width: "100%",
          height: "70rem"
        },
        menuBarPosition: "top",
        loadImage: {
          path: 'https://i.imgur.com/okbPT0k.jpg',
          name: 'SampleImage'
        },
      },
      selectionStyle: {
        cornerSize: 20,
        rotatingPointOffset: 70
      },
      usageStatistics: false
    });
  }

  componentWillUnmount() {
    // this.unbindEventHandlers();
    this.imageEditorInst.destroy();
    this.imageEditorInst = null;
  }

  render() {
    return <div ref={this.rootEl} />;
  }
}

export default function App() {
  return (
    <div>
      <Container>
        <Row>
          <Col>

    <MDBCard>
      <MDBCard>
        <MDBCardBody>
          <MDBCardTitle>Panel title</MDBCardTitle>
          <MDBCardTitle subtitle className='mb-2 text-muted'>
            Panel subtitle
          </MDBCardTitle>
          <MDBCardText>
            Some quick example text to build on the panel title and make up the bulk of the panel's content.
          </MDBCardText>
          <MDBCardLink href='#'>Panel link</MDBCardLink>
          <MDBCardLink href='#'>Another link</MDBCardLink>
        </MDBCardBody>
      </MDBCard>
    </MDBCard>
          
          </Col>
        </Row>
        <Row><Col>
          <ImageEditor />
        </Col></Row>
      </Container>
    </div>
  );
}
