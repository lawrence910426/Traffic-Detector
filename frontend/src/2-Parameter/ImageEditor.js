import React from 'react';
import PropTypes from 'prop-types';

import TuiImageEditor from "tui-image-editor";
import axios from 'axios'
import config from '../utils/config'

class ImageEditor extends React.Component {
    rootEl = React.createRef();
    imageEditorInst = null;

    removeByClassName(className) {
      var element = document.getElementsByClassName(className)
      for (var i = 0; i < element.length; i++) {
        element[i].remove()
      }
    }

    async componentDidMount() {
      this.imageEditorInst = new TuiImageEditor(this.rootEl.current, {
        includeUI: {
          menu: ['icon'],
          initMenu: "icon",
          uiSize: {
            width: "100%",
            height: "50rem"
          },
          menuBarPosition: "bottom"
        },
        selectionStyle: {
          cornerSize: 20,
          rotatingPointOffset: 70
        },
        usageStatistics: true
      });
      
      var imgLink = await axios.get(config.host + 'first_frame', {
        params: { id: this.props.video }
      })
      imgLink = imgLink.data.link

      await this.imageEditorInst.loadImageFromURL(imgLink, 'SampleImage')
      this.imageEditorInst.registerIcons({
        detectionLine: `
          M 0 0 L 0 185 L -5 185 L -5 0 L 0 0

          M 0 0 L 20 20 L 20 25 L 0 5 L 0 0
          M 0 20 L 20 40 L 20 45 L 0 25 L 0 0
          M 0 40 L 20 60 L 20 65 L 0 45 L 0 0
          M 0 60 L 20 80 L 20 85 L 0 65 L 0 0
          M 0 80 L 20 100 L 20 105 L 0 85 L 0 0
          M 0 100 L 20 120 L 20 125 L 0 105 L 0 0
          M 0 120 L 20 140 L 20 145 L 0 125 L 0 0
          M 0 140 L 20 160 L 20 165 L 0 145 L 0 0
          M 0 160 L 20 180 L 20 185 L 0 165 L 0 0
          M -5 180 L 20 200 L 20 205 L -5 185 L 0 0
          Z
        `
      })
      var objectProps = await this.imageEditorInst.addIcon('detectionLine')
      this.iconId = objectProps.id

      await this.imageEditorInst.setObjectPosition(this.iconId, {
          x: 100, y: 100, originX: 'left', originY: 'top'
      })
      await this.imageEditorInst.changeIconColor(this.iconId, '#FF0000')

      const updatePosition = () => {
        var A = this.imageEditorInst.getObjectPosition(this.iconId, 'left', 'top')
        var B = this.imageEditorInst.getObjectPosition(this.iconId, 'right', 'bottom')
        this.props.detector(A.x, A.y, B.x, B.y)
      }; 
      this.imageEditorInst.on('objectMoved', updatePosition);
      this.imageEditorInst.on('objectRotated', updatePosition);
      this.imageEditorInst.on('objectScaled', updatePosition);

      this.removeByClassName("tui-image-editor-header-logo")
      this.removeByClassName("tui-image-editor-header-buttons")
      this.removeByClassName("tui-image-editor-submenu")
      this.removeByClassName("tui-image-editor-menu")
      this.removeByClassName("tui-image-editor-help-menu")
    }
  
    componentWillUnmount() {
      this.imageEditorInst.destroy();
    }
  
    render() {
      return <div ref={this.rootEl} />;
    }
}

ImageEditor.propTypes = {
  video: PropTypes.string,
  detector: PropTypes.func
};

export default ImageEditor;
