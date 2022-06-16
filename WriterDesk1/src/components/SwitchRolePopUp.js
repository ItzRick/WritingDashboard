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

import { AdminPanelSettingsOutlined, BiotechOutlined, SchoolOutlined } from '@mui/icons-material';

const RoleDialog = ({userRole}) => {
    const[open, setOpen] = useState(false);
    const [value, setValue] = useState(userRole);

    const onClose = (value) => {
        setOpen(false);
        if (value) {
            setValue(value);
        }
    }
    
    const handleCancel = () => {
        onClose();
    }
    
    const handleOk = () => {
       onClose(value);
    };

    const handleListItemClick = (value) => {
        setValue(value);
    }

    const handleClickOpen = () => {
        setOpen(true);
    }

    return (
        <>
            <div onClick={handleClickOpen}>{value}</div>
            <Dialog
                open={open}

                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                    {"Set user role"}
                </DialogTitle>
                <List>
                    <ListItem button onClick={() => handleListItemClick('Student')} selected={value === 'student'}>
                        <ListItemAvatar>
                            <Avatar>
                                <SchoolOutlined />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary="Student" />
                    </ListItem>
                    <ListItem button onClick={() => handleListItemClick('Researcher')} selected={value === 'researcher'}>
                        <ListItemAvatar>
                            <Avatar>
                                <BiotechOutlined />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary="Researcher" />
                    </ListItem>
                    <ListItem button onClick={() => handleListItemClick('Admin')} selected={value === 'admin'}>
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