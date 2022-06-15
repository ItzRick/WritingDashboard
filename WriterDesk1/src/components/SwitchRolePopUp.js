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

/**
 * Popup with button
 * 
 * @param {func} func function activated when main button is clicked
 * 
 * @returns popup with button for upload page
 */
function RoleDialog(props) {
    const {onClose, selectedValue, open} = props;
    const [value, setValue] = useState(selectedValue);
    
    const handleCancel = () => {
        onClose();
    }
    
    const handleOk = () => {
       onClose(value);
    };

    const handleListItemClick = (value) => {
        setValue(value);
    }

    return (
        <>
            <Dialog
                open={open}

                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                    {"Set user role"}
                </DialogTitle>
                <List>
                    <ListItem button onClick={() => handleListItemClick('student')} selected={value === 'student'}>
                        <ListItemAvatar>
                            <Avatar>
                                <SchoolOutlined />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary="Student" />
                    </ListItem>
                    <ListItem button onClick={() => handleListItemClick('researcher')} selected={value === 'researcher'}>
                        <ListItemAvatar>
                            <Avatar>
                                <BiotechOutlined />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText primary="Researcher" />
                    </ListItem>
                    <ListItem button onClick={() => handleListItemClick('admin')} selected={value === 'admin'}>
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