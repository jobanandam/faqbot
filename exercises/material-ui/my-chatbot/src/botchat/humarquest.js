import React from 'react';
import Grid from '@material-ui/core/Grid';
import ChatLine from '../chatline/chatline';

export default function MessageBox() {

  return (
    <React.Fragment>
        <Grid item xs={6}></Grid>
        <Grid item xs={6}>
              <ChatLine text="Hello Bot! May I know the procedure to get access to JIRA?"></ChatLine>
        </Grid>
    </React.Fragment>
  );
}
