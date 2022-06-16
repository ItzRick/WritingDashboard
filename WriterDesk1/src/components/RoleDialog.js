import { useState } from 'react';

import '../css/roledialog.css'

import {
    Dialog,
    DialogActions,
    DialogTitle,
    Button,
} from '@mui/material';

import Avatar from '@mui/material/Avatar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';

import { AdminPanelSettingsOutlined, MoreHorizOutlined, BiotechOutlined, SchoolOutlined } from '@mui/icons-material';

import axios from 'axios';
import { authHeader } from '../helpers/auth-header';


/**
 * This function sends a request to the server where we ask to change the role for a specific user
 * 
 * @param {int} userId ID of user of whom we want to change the role
 * @param {String} newRole intended role of the user
 * @returns Promise of axios post request where we try to change the role of the user
 */
const ChangeRole = (userId, newRole) => {
    // url for request
    const url = 'https://127.0.0.1:5000/loginapi/setRole';

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

    // handle conformation of selection
    const handleOk = () => {
        onClose(selectedValue);
        // Send request and handle possible error
        ChangeRole(userId, selectedValue.toLowerCase()).catch((error) => {
            setValue(userRole);
            let alertText = "Error while changing role: \n" + error.message;
            alert(alertText);
        });
     };
    
     // handle cancel of selection
    const handleCancel = () => {
        onClose();
    }


    return (
        <>
            <div title={"Change role of user"} className={"roleColumn"} onClick={handleClickOpen}>{value } <MoreHorizOutlined/></div>
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
                    <ListItem button onClick={() => handleListItemClick('Student')} selected={selectedValue === 'Student'}>
                        <ListItemAvatar>
                            <Avatar>
                                <SchoolOutlined />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary="Student" />
                    </ListItem>
                    <ListItem button onClick={() => handleListItemClick('Researcher')} selected={selectedValue === 'Researcher'}>
                        <ListItemAvatar>
                            <Avatar>
                                <BiotechOutlined />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary="Researcher" />
                    </ListItem>
                    <ListItem button onClick={() => handleListItemClick('Admin')} selected={selectedValue === 'Admin'}>
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