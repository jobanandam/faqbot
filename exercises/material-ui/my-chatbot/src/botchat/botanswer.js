import React from 'react';
import Grid from '@material-ui/core/Grid';
import ChatLine from '../chatline/chatline';

export default function MessageBox() {

  return (
    <React.Fragment>
        <Grid item xs={6}>
              <ChatLine text="Hello User! How may I help you ?"></ChatLine>
        </Grid>
        <Grid item xs={6}></Grid>
    </React.Fragment>
  );
}
