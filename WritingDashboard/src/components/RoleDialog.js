import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import '../css/roledialog.css'

import {
    Avatar,
    Dialog,
    DialogActions,
    DialogTitle,
    Button,
    List,
    ListItem,
    ListItemAvatar,
    ListItemText,
} from '@mui/material';

import { AdminPanelSettingsOutlined, MoreHorizOutlined, BiotechOutlined, SchoolOutlined } from '@mui/icons-material';

import axios from 'axios';
import { authHeader } from '../helpers/auth-header';
import { AuthenticationService } from '../services/authenticationService';
import AlertDialog from "./AlertDialog";


/**
 * This function sends a request to the server where we ask to change the role for a specific user
 * 
 * @param {int} userId ID of user of whom we want to change the role
 * @param {String} newRole intended role of the user
 * @returns Promise of axios post request where we try to change the role of the user
 */
const ChangeRole = (userId, newRole) => {
    // url for request
    const url = '/api/loginapi/setRole';

    // data for request
    const formData = new FormData();
    formData.append('userId', userId);
    formData.append('newRole', newRole)

    return axios.post(url, formData, {
        headers: authHeader(), // Autheader needed for request
    });
}

/**
 * Dialog component (pop up) where a new role can be set for user.
 * Request to server is send to change role.
 * 
 * @param {String} userRole     current userole of user
 * @param {Integer} userId      userid of user
 * @param {String} userName     username of user
 * @returns Dialog component where a new userRole can be selected for user with id: userId
 */
const RoleDialog = ({userRole, userId, userName}) => {
    // popup shown
    const[open, setOpen] = useState(false);
    // current/set role value for user
    const [value, setValue] = useState(userRole); 
     // new role value for user
    const [selectedValue, setSelected] = useState(userRole);

    // Show dialog when changing own role
    const [showChangeOwnRoleDialog, setShowChangeOwnRoleDialog] = useState(false);
    // Show error dialog when error occurred in setRole call
    const [showErrorDialog, setShowErrorDialog] = useState(false);
    // Alert message given by the setRole backend call when there is an error
    const [alertMessage, setAlertMessage] = useState('');

    // handle opening of popup
    const handleClickOpen = () => {
        setSelected(value);
        setOpen(true);
    }
    
    // handle closing of popup; Set new role if given
    const onClose = (value) => {
        setOpen(false);
        if (value) {
            setValue(value);
        }
    }

    // handle selection of item
    const handleListItemClick = (value) => {
        setSelected(value);
    }

    let navigate = useNavigate();

    /**
     * Show dialog when changing own role, otherwise change role immediately.
     */
    const handleOk = () => {
        if (AuthenticationService.getCurrentUserId() === userId) {
            setShowChangeOwnRoleDialog(true);
        } else {
            onClose(selectedValue);
            callChangeRole();
        }

     };

    /**
     * First unshow alert dialog, then call change role function with the correct parameters.
     */
    const callChangeRole = () => {
        // Don't show dialog anymore if it was displayed.
        setShowChangeOwnRoleDialog(false);

        // Send request and handle possible error
        ChangeRole(userId, selectedValue.toLowerCase()).then(r => {
            if(AuthenticationService.getCurrentUserId() === userId && selectedValue !== 'admin') {
                AuthenticationService.logout();  // If admin role is changed to another role, logout
                navigate("../Login", {replace: true});
            }
        }).catch((error) => {
            // Reset shown role to previous role
            setValue(userRole);

            // Show alert dialog with error message
            setAlertMessage(error.response.data);
            setShowErrorDialog(true);
        });

    }
    
     // handle cancel of selection
    const handleCancel = () => {
        onClose();
    }


    return (
        <>
            {showChangeOwnRoleDialog &&
              <AlertDialog title = "Change own role" text = "You're about to change your own role. Do you want to continue?"
                           buttonAgree={<Button style={{color: "red"}} onClick={(e) => {onClose(selectedValue); callChangeRole();}}>Yes</Button>}
                           buttonCancel={<Button onClick={(e) => {setShowChangeOwnRoleDialog(false)}}>Cancel</Button>}
              />}
            {showErrorDialog &&
              <AlertDialog title = "Error while changing role" text = {alertMessage}
                           buttonAgree={<Button style={{color: "red"}} onClick={(e) => {setShowErrorDialog(false)}}>Ok</Button>}
              />}
            {/* clickable and ... only for non-participants */}
            {userRole !== 'participant' && <div title={"Change role of user"} className={"roleColumn"} onClick={handleClickOpen}> { value } <MoreHorizOutlined/> </div>}
            {userRole === 'participant' && <div title={"Cannot change role of participant"} className={"roleColumn"}> { value } </div>}
            <Dialog
                fullWidth={true}
                maxWidth='xs'

                open={open}

                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                    {"New role for: " + userName}
                </DialogTitle>
                <List sx={{ pt: 0 }}>
                    <ListItem button onClick={() => handleListItemClick('student')} selected={selectedValue === 'student'}>
                        <ListItemAvatar>
                            <Avatar>
                                <SchoolOutlined />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary="Student" />
                    </ListItem>
                    <ListItem button onClick={() => handleListItemClick('researcher')} selected={selectedValue === 'researcher'}>
                        <ListItemAvatar>
                            <Avatar>
                                <BiotechOutlined />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary="Researcher" />
                    </ListItem>
                    <ListItem button onClick={() => handleListItemClick('admin')} selected={selectedValue === 'admin'}>
                        <ListItemAvatar>
                            <Avatar>
                                <AdminPanelSettingsOutlined />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary="Admin" />
                    </ListItem>
                </List>

                <DialogActions>
                    <Button autoFocus onClick={handleCancel}>
                        Cancel
                    </Button>
                    <Button onClick={handleOk}>Ok</Button>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default RoleDialog;