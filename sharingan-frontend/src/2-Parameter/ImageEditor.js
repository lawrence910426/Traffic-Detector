import TuiImageEditor from "tui-image-editor";
import React from 'react';

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
      this.imageEditorInst.destroy();
    }
  
    render() {
      return <div ref={this.rootEl} />;
    }
}

export default ImageEditor;