import './App.css';
import Dropzone from "dropzone";
import React from 'react';

Dropzone.autoDiscover = false;

class Upload extends React.Component {
  render() {
    return (
      <div 
        id="Upload_Box"
        className="d-xl-flex justify-content-xl-center align-items-xl-center needsclick dz-clickable" 
        action="/">
      </div>
    );
  }

  componentDidMount() {
    /* let myDropzone = new Dropzone("#Upload_Box");
    myDropzone.on("addedfile", file => {
      console.log(`File added: ${file.name}`);
    }); */
  }
}

export default Upload;
