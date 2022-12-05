import React from 'react';
import PropTypes from 'prop-types';

import Dropzone from 'react-dropzone'
import { MDBIcon } from 'mdb-react-ui-kit';
import config from '../utils/config'
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import axios from 'axios';

Dropzone.autoDiscover = false;

class Upload extends React.Component {
  constructor() {
    super();
    this.state = { progress: 0 };
  }

  async droppedFiles(files) {
    var fileObj = files[0]
    console.log(fileObj)

    var vid = await this.uploadFileServer(fileObj);
    this.props.video(vid)

    this.props.next();
  }

  async uploadFileServer(file) { 
      let formData = new FormData(); 
      formData.append("file", file);

      let resp = await axios.request({
          method: "post", 
          url: config.host + "upload", 
          data: formData, 
          onUploadProgress: (p) => {
            console.log(p); 
            this.setState({
              progress: p.loaded / p.total * 100
            })
          }
      })

      this.setState({
        progress: 100,
      })

      return resp.data.id
  }

  renderProgressBar() {
    if (this.state.progress != 0) {
      return (
        <Row style={{ marginTop: '1rem' }}>
          <Col xs={6} md={2}><label>影片上傳進度：</label></Col>
          <Col>
            <div className="progress" style={{height: '20px'}}>
              <div className="progress-bar" 
                  role="progressbar" 
                  style={{width: this.state.progress + '%'}} 
                  aria-valuenow={this.state.progress} 
                  aria-valuemin="0" aria-valuemax="100">
                  {Math.floor(this.state.progress)}%
              </div>
            </div>
          </Col>
        </Row>
      )
    }
  }

  render() {
    return (
      <div>
        <Dropzone onDrop={this.droppedFiles.bind(this)}>
          {({getRootProps, getInputProps}) => (
            <section>
              <div {...getRootProps()} style={{
                borderStyle: 'dashed',
                height: '20rem'
              }}>
                <input {...getInputProps()} />
                <p style={{
                  textAlign: 'center',
                  marginTop: '3rem'
                }}>將檔案拖曳到此以上傳影片</p>

                <MDBIcon fas icon="cloud-upload-alt" style={{
                  textAlign: 'center',
                  width: '100%',
                  fontSize: '10rem',
                  marginTop: '1rem'
                }} />
              </div>
            </section>
          )}
        </Dropzone>

        { this.renderProgressBar() }
      </div>
    );
  }
}

Upload.propTypes = {
  next: PropTypes.func,
  video: PropTypes.func
};

export default Upload;
