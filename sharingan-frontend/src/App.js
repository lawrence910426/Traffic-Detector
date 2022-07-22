import * as React from 'react';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Button from '@mui/material/Button';

import Upload from './1-Upload/Upload'
import Parameter from './2-Parameter/Parameter'
import Results from './3-Results/Results'

import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

const steps = ['上傳影片', '設置參數', '下載結果'];

export default function App() {
  const [activeStep, setActiveStep] = React.useState(0);

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  }

  const getStepContent = () => {
    if(activeStep === 0) return (<Upload next={handleNext}></Upload>)
    if(activeStep === 1) return (<Parameter next={handleNext}></Parameter>)
    if(activeStep === 2) return (<Results reset={handleReset}></Results>)
  }

  return (
    <Box sx={{ width: '100%' }}>
      <Stepper activeStep={activeStep}>
        {steps.map((label) => {
          const stepProps = {};
          const labelProps = {};
          return (
            <Step key={label} {...stepProps}>
              <StepLabel {...labelProps}>{label}</StepLabel>
            </Step>
          );
        })}
      </Stepper>
      
      <React.Fragment>
        <Container style={{marginTop: '5rem'}}><Row><Col>
          {getStepContent(activeStep)}
        </Col></Row></Container>

        <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
          <Box sx={{ flex: '1 1 auto' }} />
        </Box>
      </React.Fragment>
    </Box>
  );
}
