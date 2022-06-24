import {
    useState,
} from 'react';

import {
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
} from '@mui/material';

import BlueButton from "./BlueButton";

/**
 * Popup with button
 * 
 * @param {func} func function activated when main button is clicked
 * 
 * @returns popup with button for upload page
 */
const UploadPopUp = ({func}) => {
    // whether popup is open
    const [open, setOpen] = useState(false);

    // change state of popup
    const switchOpen = () => {
        setOpen(val => !val);
    }

    // handle opening of popup
    const handleClickOpen = () => {
        func();
        switchOpen();
    };

    return (
        <>
            <BlueButton idStr='uploadYourDocument(s)' addStyle={{ fontSize: '2vw', textTransform: 'none' }} onClick={handleClickOpen}>Upload your document(s)</BlueButton>
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
                    <BlueButton idStr='uploadMoreDocuments' onClick={switchOpen}> Upload more documents </BlueButton>
                    <BlueButton idStr='viewDocuments' pathName='/Documents'> View documents </BlueButton>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default UploadPopUp;