import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import ButtonAppBar from '../chatheader/chatheader';
import BotAnswer from '../botchat/botanswer';
import HumanQuest from '../botchat/humarquest';

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
}));

export default function MessageBox() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={12}><ButtonAppBar/></Grid>
          <BotAnswer /><HumanQuest />
          <BotAnswer /><HumanQuest />
      </Grid>
    </div>
  );
}
