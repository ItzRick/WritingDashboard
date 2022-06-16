import { useState, useEffect, useRef } from 'react';

import {
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
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

const ChangeRole = (userId, newRole) => {
    const url = 'https://127.0.0.1:5000/loginapi/setRole';

    const formData = new FormData();
    formData.append('userId', userId);
    formData.append('newRole', newRole)

    return axios.post(url, formData, {
        headers: authHeader(),
    });
}

const RoleDialog = ({params}) => {
    const userRole = params.row.role;
    const userId = params.id;
    const userName = params.row.username;

    const[open, setOpen] = useState(false);
    const [value, setValue] = useState(userRole);
    const [selectedValue, setSelected] = useState(userRole);

    const handleClickOpen = () => {
        setSelected(value);
        setOpen(true);
    }
    
    const onClose = (value) => {
        setOpen(false);
        if (value) {
            setValue(value);
        }
    }

    const handleListItemClick = (value) => {
        setSelected(value);
    }

    const handleOk = () => {
        onClose(selectedValue);
        ChangeRole(userId, selectedValue.toLowerCase()).catch((error) => {
            setValue(userRole);
            let alertText = "Error while changing role: \n" + error.message;
            alert(alertText);
        });
     };
    
    const handleCancel = () => {
        onClose();
    }


    return (
        <>
            <div onClick={handleClickOpen} style={{width: 130, display:'flex', alignItems:'center', flexWrap: 'wrap', justifyContent: 'space-between'}}>{value } <MoreHorizOutlined/></div>
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