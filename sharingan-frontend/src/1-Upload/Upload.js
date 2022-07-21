import React from 'react';
import Dropzone from 'react-dropzone'

import { MDBIcon } from 'mdb-react-ui-kit';

Dropzone.autoDiscover = false;

class Upload extends React.Component {
  render() {
    return (
      <div>
        <Dropzone onDrop={this.droppedFiles}>
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

  droppedFiles(acceptedFiles) {
    console.log(acceptedFiles)
  }
}

export default Upload;
