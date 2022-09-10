import React from "react";

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import { MDBCard, MDBCardBody, MDBCardTitle, MDBBtn } from 'mdb-react-ui-kit';

class ModelSelection extends React.Component {
  constructor() {
    super();
    this.state = {
      selectedModel: "full-model"
    };
  }

  toggleModel(modelName) { this.setState({ selectedModel: modelName }); }

  render() {
    return (
      <Row>
        <Col>
          <MDBCard style={{
            backgroundColor: this.state.selectedModel === "full-model" ? "lightgrey" : "white"
          }}>
            <MDBCardBody>
              <MDBCardTitle>完整模型</MDBCardTitle>
              <ul>
                <li>適合作為報告輸出</li>
                <li>符合工研院標準</li>
                <li>每分鐘的影片約需要三分鐘處理</li>
              </ul>
              <MDBBtn onClick={() => { this.toggleModel('full-model') }}>使用完整模型</MDBBtn>
            </MDBCardBody>
          </MDBCard>
        </Col>

        <Col>
          <MDBCard style={{
            backgroundColor: this.state.selectedModel === "mini-model" ? "lightgrey" : "white"
          }}>
            <MDBCardBody>
              <MDBCardTitle>預覽模型</MDBCardTitle>
              <ul>
                <li>適合調整鏡頭角度</li>
                <li>不符合工研院標準</li>
                <li>每分鐘的影片約需要十秒鐘處理</li>
              </ul>
              <MDBBtn onClick={() => { this.toggleModel('mini-model') }}>使用預覽模型</MDBBtn>
            </MDBCardBody>
          </MDBCard>
        </Col>
      </Row>
    );
  }
}

export default ModelSelection;