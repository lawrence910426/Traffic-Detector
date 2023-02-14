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

    async StraightWidgets() {
      this.redId = (await this.imageEditorInst.addIcon('detectionLineHori')).id
      this.greenId = (await this.imageEditorInst.addIcon('detectionLineHori')).id
      
      await this.imageEditorInst.changeIconColor(this.redId, '#FF0000')
      await this.imageEditorInst.changeIconColor(this.greenId, '#00FF00')

      await this.imageEditorInst.setObjectPosition(this.redId, {
        x: 50, y: 50, originX: 'left', originY: 'top'
      })
      await this.imageEditorInst.setObjectPosition(this.greenId, {
        x: 50, y: 100, originX: 'left', originY: 'top'
      })

      const updatePosition = () => {
        var colorIdMapping = {
          'X': this.redId,
          'Y': this.greenId
        }
        var detector = {}
        for (var k in colorIdMapping) {
          var A = this.imageEditorInst.getObjectPosition(colorIdMapping[k], 'left', 'top')
          var B = this.imageEditorInst.getObjectPosition(colorIdMapping[k], 'right', 'bottom')
          detector[k] = {
            x1: Math.max(0, Math.floor(A.y)), y1: Math.max(0, Math.floor(A.x)),
            x2: Math.max(0, Math.floor(B.y)), y2: Math.max(0, Math.floor(B.x))
          }
        }
        this.props.updateDetectorCallback(detector)
      }; 
      return updatePosition
    }

    async TWidgets() {
      this.redId = (await this.imageEditorInst.addIcon('detectionLineHori')).id
      this.greenId = (await this.imageEditorInst.addIcon('detectionLineVert')).id
      this.blueId = (await this.imageEditorInst.addIcon('detectionLineVert')).id
      
      await this.imageEditorInst.changeIconColor(this.redId, '#FF0000')
      await this.imageEditorInst.changeIconColor(this.greenId, '#00FF00')
      await this.imageEditorInst.changeIconColor(this.blueId, '#0000FF')

      await this.imageEditorInst.setObjectPosition(this.redId, {
        x: 150, y: 50, originX: 'left', originY: 'top'
      })
      await this.imageEditorInst.setObjectPosition(this.blueId, {
        x: 100, y: 100, originX: 'left', originY: 'top'
      })
      await this.imageEditorInst.setObjectPosition(this.greenId, {
        x: 400, y: 100, originX: 'left', originY: 'top'
      })

      const updatePosition = () => {
        var colorIdMapping = {
          'A': this.blueId,
          'B': this.greenId,
          'T': this.redId,
        }
        var detector = {}
        for (var k in colorIdMapping) {
          var A = this.imageEditorInst.getObjectPosition(colorIdMapping[k], 'left', 'top')
          var B = this.imageEditorInst.getObjectPosition(colorIdMapping[k], 'right', 'bottom')
          detector[k] = {
            x1: Math.max(0, Math.floor(A.y)), y1: Math.max(0, Math.floor(A.x)),
            x2: Math.max(0, Math.floor(B.y)), y2: Math.max(0, Math.floor(B.x))
          }
        }
        this.props.updateDetectorCallback(detector)
      }; 
      return updatePosition
    }

    async CrossWidgets() {
      this.redId = (await this.imageEditorInst.addIcon('detectionLineHori')).id
      this.orangeId = (await this.imageEditorInst.addIcon('detectionLineHori')).id
      this.greenId = (await this.imageEditorInst.addIcon('detectionLineVert')).id
      this.blueId = (await this.imageEditorInst.addIcon('detectionLineVert')).id
      
      await this.imageEditorInst.changeIconColor(this.redId, '#FF0000')
      await this.imageEditorInst.changeIconColor(this.greenId, '#00FF00')
      await this.imageEditorInst.changeIconColor(this.blueId, '#0000FF')
      await this.imageEditorInst.changeIconColor(this.orangeId, '#FF7F00')

      await this.imageEditorInst.setObjectPosition(this.redId, {
        x: 150, y: 100, originX: 'left', originY: 'top'
      })
      await this.imageEditorInst.setObjectPosition(this.blueId, {
        x: 100, y: 150, originX: 'left', originY: 'top'
      })
      await this.imageEditorInst.setObjectPosition(this.orangeId, {
        x: 150, y: 400, originX: 'left', originY: 'top'
      })
      await this.imageEditorInst.setObjectPosition(this.greenId, {
        x: 400, y: 150, originX: 'left', originY: 'top'
      })

      const updatePosition = () => {
        var colorIdMapping = {
          'A': this.blueId,
          'B': this.greenId,
          'X': this.redId,
          'Y': this.orangeId
        }
        var detector = {}
        for (var k in colorIdMapping) {
          var A = this.imageEditorInst.getObjectPosition(colorIdMapping[k], 'left', 'top')
          var B = this.imageEditorInst.getObjectPosition(colorIdMapping[k], 'right', 'bottom')
          detector[k] = {
            x1: Math.max(0, Math.floor(A.y)), y1: Math.max(0, Math.floor(A.x)),
            x2: Math.max(0, Math.floor(B.y)), y2: Math.max(0, Math.floor(B.x))
          }
        }
        this.props.updateDetectorCallback(detector)
      }; 
      return updatePosition
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

      this.imageEditorInst.registerIcons({
        detectionArea: `
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
        `, detectionLineVert: `
          M 0 0 L 0 200 L -5 200 L -5 0 L 0 0
        `, detectionLineHori: `
          M 0 0 L 200 0 L 200 -5 L 0 -5 L 0 0
        `
      })
      
      try {
        var imgLink = await axios.get(config.host + 'first_frame', {
          params: { id: this.props.video }
        })
        imgLink = imgLink.data.link
  
        await this.imageEditorInst.loadImageFromURL(imgLink, 'SampleImage')
      } catch (error) {
        console.log("Failed to fetch first frame " + error)
      }
      

      this.removeByClassName("tui-image-editor-header-logo")
      this.removeByClassName("tui-image-editor-header-buttons")
      this.removeByClassName("tui-image-editor-submenu")
      this.removeByClassName("tui-image-editor-menu")
      this.removeByClassName("tui-image-editor-help-menu")

      var updatePosition;
      if (this.props.mode == 'straight') {
        updatePosition = await this.StraightWidgets();
      } else if (this.props.mode == 't_intersection') {
        updatePosition = await this.TWidgets();
      } else if (this.props.mode == 'cross_intersection') {
        updatePosition = await this.CrossWidgets();
      }
      
      this.imageEditorInst.on('objectMoved', updatePosition);
      this.imageEditorInst.on('objectRotated', updatePosition);
      this.imageEditorInst.on('objectScaled', updatePosition);
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
  mode: PropTypes.string,
  updateDetectorCallback: PropTypes.func
};

export default ImageEditor;
