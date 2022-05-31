import {
    useState,
} from 'react';

import { Link } from 'react-router-dom';

import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
} from '@mui/material';

import BlueButton from "./BlueButton";

/**
 * 
 * @param {func} onAgree function that has to be activated when the accept has been clicked, default is empty function
 * @param {func} onDisagree function that has to be activated when the cancel has been clicked, default is empty function
 * 
 * @returns 
 */
const UploadPopUp = ({func}) => {
    const [open, setOpen] = useState(false);

    const switchOpen = () => {
        setOpen(val => !val);
    }

    const handleClickOpen = () => {
        switchOpen();
        func();
    };


    return (
        <>
            <BlueButton addStyle={{ fontSize: '2vw', textTransform: 'none' }} onClick={handleClickOpen}>Upload your document(s)</BlueButton>
            <Dialog
                open={open}
                onClose={switchOpen}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                    {"Upload your documents?"}
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        Uploading successful. What would you like to do next?
                    </DialogContentText>
                </DialogContent>
                <DialogActions sx={{justifyContent:'space-between'}}>
                    <BlueButton onClick={switchOpen}> Upload more documents </BlueButton>
                    <BlueButton pathName='/Documents'> View documents </BlueButton>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default UploadPopUp;