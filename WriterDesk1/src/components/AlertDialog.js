import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';


// routing
import { Link, Outlet } from 'react-router-dom';


/**
 * AlertDialog that is shown on top of page. This shows a dialog with a title and text and two buttons that can be clicked.
 * @property title - Title shown in the alert dialog
 * @property text - Body shown in the alert dialog
 * @property buttonCancel - Button component to cancel
 * @property buttonAgree - Button component to agree
 * @returns AlertDialog component
 */
const AlertDialog = (props) => {
  return (
    <div>
      <Dialog
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
        open={true}>
        <DialogTitle id="alert-dialog-title">
          {props.title}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            {props.text}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          {props.buttonCancel}
          {props.buttonAgree}
        </DialogActions>
      </Dialog>
    </div>
  )
}

export default AlertDialog;