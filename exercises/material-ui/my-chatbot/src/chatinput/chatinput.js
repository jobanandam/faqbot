import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import SendRoundedIcon from '@material-ui/icons/SendRounded';

const useStyles = makeStyles(theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
    marginTop : 20
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 200,
  },
  dense: {
    marginTop: 19,
  },
  menu: {
    width: 200,
  },
  button: {
    margin: theme.spacing(1),
  },
}));


export default function TextFields() {
  const classes = useStyles();

  return (
    <form className={classes.container} noValidate autoComplete="off">
      <Grid container spacing={2}>
        <Grid item xs={10}>
            <TextField
            id="standard-full-width"
            style={{ margin: 8 }}
            placeholder="What's in your mind shoot?"
            fullWidth
            margin="normal"
            InputLabelProps={{
              shrink: true,
            }}
            />
        </Grid>
        <Grid item xs={2}>
            <Button
            variant="contained"
            color="primary"
            className={classes.button}
            endIcon={<SendRoundedIcon />}>Send</Button>
        </Grid>
      </Grid>
    </form>
  );
}
