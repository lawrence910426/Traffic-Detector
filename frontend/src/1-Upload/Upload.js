import React from 'react';
import PropTypes from 'prop-types';

import Dropzone from 'react-dropzone'
import { MDBIcon } from 'mdb-react-ui-kit';
import config from '../utils/config'

Dropzone.autoDiscover = false;

class Upload extends React.Component {
  async droppedFiles(files) {
    var fileObj = files[0]

    var vid = await this.uploadFileServer(fileObj);
    this.props.video(vid)

    this.props.next();
  }

  async uploadFileServer(file) {
      let formData = new FormData(); 
      formData.append("file", file);
      var ans = await fetch(config.host + "upload", {
          method: "POST", 
          body: formData
      }); 
      ans = await ans.json()
      return ans.id
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
      </div>
    );
  }
}

Upload.propTypes = {
  next: PropTypes.func,
  video: PropTypes.func
};

export default Upload;
