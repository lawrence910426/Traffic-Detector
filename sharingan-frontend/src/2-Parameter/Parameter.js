import React, { useState, useEffect, useRef } from "react";
import TuiImageEditor from "tui-image-editor";

import "tui-image-editor/dist/tui-image-editor.css";
import "tui-color-picker/dist/tui-color-picker.css";

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { MDBCard, MDBCardBody, MDBCardTitle, MDBCardText, MDBBtn } from 'mdb-react-ui-kit';

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
            <MDBCard background='info'>
              <MDBCardBody>
                <MDBCardTitle>完整模型</MDBCardTitle>
                <MDBCardText>
                  <ul>
                    <li>適合作為報告輸出</li>
                    <li>符合工研院標準</li>
                    <li>每分鐘的影片約需要三分鐘處理</li>
                  </ul>
                </MDBCardText>
                <MDBBtn href='#'>使用完整模型</MDBBtn>
              </MDBCardBody>
            </MDBCard>
          </Col>

          <Col>
            <MDBCard>
              <MDBCardBody>
                <MDBCardTitle>預覽模型</MDBCardTitle>
                <MDBCardText>
                  <ul>
                    <li>適合調整鏡頭角度</li>
                    <li>不符合工研院標準</li>
                    <li>每分鐘的影片約需要十秒鐘處理</li>
                  </ul>                
                </MDBCardText>
                <MDBBtn href='#'>使用預覽模型</MDBBtn>
              </MDBCardBody>
            </MDBCard>
           </Col>
        </Row>

        <Row style={{ marginTop: '3rem' }}><Col>
          <ImageEditor />
        </Col></Row>
      </Container>
    </div>
  );
}
