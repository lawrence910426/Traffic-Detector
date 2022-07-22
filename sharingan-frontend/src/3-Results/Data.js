import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';

import { MDBBtn, MDBTable, MDBTableBody, MDBTableHead } from 'mdb-react-ui-kit';
import React from 'react';

import { utils } from 'xlsx';

class Data extends React.Component {
  constructor() {
    super()
    var worksheet = utils.json_to_sheet([
        { S:1, h:2,           t:5, J:6, S_1:7 },
        { S:2, h:3,           t:6, J:7, S_1:8 },
        { S:3, h:4,           t:7, J:8, S_1:9 },
        { S:4, h:5, e:6, e_1:7, t:8, J:9, S_1:0 }
      ], {header:["S","h","e","e_1","t","J","S_1"]}
    );
    var html = utils.sheet_to_html(worksheet);
    this.state = { sheet: html }
  }

  render() {
    return (
        <Container>
            <Row>
                <Col style={{ marginTop: '1rem' }}>
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
                                <th scope='row'>小客車</th>
                                <td>23</td>
                                <td>52</td>
                            </tr>
                            <tr>
                                <th scope='row'>機車</th>
                                <td>104</td>
                                <td>203</td>
                            </tr>
                            <tr>
                                <th scope='row'>大車</th>
                                <td>104</td>
                                <td>203</td>
                            </tr>
                            <tr>
                                <th scope='row'>連結車</th>
                                <td>3</td>
                                <td>7</td>
                            </tr>
                            <tr>
                                <th scope='row'>MCU</th>
                                <td>1033</td>
                                <td>1523</td>
                            </tr>
                        </MDBTableBody>

                    </MDBTable>
                    <MDBBtn>下載交通流量結果</MDBBtn>
                </Col>

                <Col style={{ marginTop: '1rem' }}>
                    <video width="100%" controls>
                        <source src="http://techslides.com/demos/sample-videos/small.mp4" type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                    <MDBBtn>下載影片</MDBBtn>
                </Col>
            </Row>

            <Row style={{ marginTop: '1rem' }}>
                <Col><MDBBtn onClick={this.props.reset}>完成分析，回到上傳影片頁面</MDBBtn></Col>
            </Row>
        </Container>
    )
  }
}

export default Data;
