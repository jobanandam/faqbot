import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import MessageBox from '../messagebox/messagebox';
import ChatInput from '../chatinput/chatinput';

export default function SimpleContainer() {
  return (
    <React.Fragment>
      <CssBaseline />
      <Container maxWidth="md">
        <Typography component="div" overflow="visible" style={{ backgroundColor: '#cfe8fc',  }}>
            <MessageBox></MessageBox>
        </Typography>
        <ChatInput />
      </Container>
    </React.Fragment>
  );
}
