// materials
import {
  Button,
  IconButton,
  Stack,
  Tooltip,
} from "@mui/material";
import {
  DeleteOutline,
  Download
} from "@mui/icons-material";

// routing
import { useOutletContext, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useState, useEffect } from 'react';
import { DataGrid } from "@mui/x-data-grid";

import RoleDialog from "./../components/RoleDialog";
import BlueButton from './../components/BlueButton';

import React from 'react';
import "../css/styles.css";
import "../css/main.css";
import { authHeader } from "../helpers/auth-header";
// Authentication service for the admin to be able to delete himself and logout:
import { AuthenticationService } from '../services/authenticationService';
import fileDownload from 'js-file-download';
import AlertDialog from "../components/AlertDialog";

/**
 * 
 * @returns Users Page
 */
const Users = () => {
    // Navigate element to be able to logout the current user:
    const navigate = useNavigate();

    const [showFailPopup, setShowFailPopup] = useState(false);
    const [failText, setFailText] = useState("");

  /**
   * Delete the user corresponding to the userId.
   * @param {userId} userId: The userId of the user that needs to be removed.
   */
  function deleteUser(userID) {
      setShowDeleteDialog(false);
      //   The backend url:
      const url = 'https://api.writingdashboard.xyz/usersapi/deleteUserAdmin';
      // Make the backend call and set the table data from the response data:
      axios.post(url,{userID: userID},{headers: authHeader()})
      .then((_response) => {
        setData();
        // If the admin has removed himself, logout:
        if (AuthenticationService.getCurrentUserId() === userID) {
            navigate("../Login", { replace: true });
        }
      })
      .catch((error) => {
        setShowFailPopup(true);
        setFailText(error.response.data);
      });
  }

  // State to keep track of the data inside the table:
  const [tableData, setTableData] = useState([])

  const [showDeleteDialog, setShowDeleteDialog] = useState(false);  // Show dialog when deleting user
  const [deleteId, setDeleteId] = useState();  // ID that is going to be deleted when pressing delete button

  const columns = [
    {
      field: 'username',
      headerName: 'Username',
      width: 350,
      editable: false,
    },
    {
      field: 'role',
      headerName: 'Role',
      width: 150,
      editable: false,
      renderCell: (params) => {
        // set arguments
        const userRole = params.row.role;
        const userId = params.row.id;
        const userName = params.row.username;
  
        // display role, and show dialog when clicked
        return <div><RoleDialog userRole={userRole} userId={userId} userName={userName}></RoleDialog></div>
      }
    },
    {
      field: "actions",
      headerName: "Actions",
      sortable: false,
      renderCell: (params) => {
        return (<div>
          <Tooltip title="Download the userdata of this user.">
            <IconButton onClick={(e) => { handleUserDataSingle(e, params) }}><Download /></IconButton>
          </Tooltip>
          <Tooltip title="Delete this user.">
            <IconButton onClick={() => { setDeleteId(params.row.id); setShowDeleteDialog(true); }}><DeleteOutline /></IconButton>
          </Tooltip>
        </div>);
      }
    }
  ];

  /**
   * Set the users in the table with an api call. 
   */
  const setData = () => {
    //   The backend url:
    const url = 'https://api.writingdashboard.xyz/usersapi/users';
    // Make the backend call and set the table data from the response data:
    axios.get(url,{headers: authHeader() })
      .then((response) => {
        setTableData(response.data)
      })
  }

  //set title in parent 'base' 
  const { setTitle } = useOutletContext();
  useEffect(() => {
    setTitle('Users');
    setData();
  }, []);

  const [selectedInstances, setSelectedInstances] = useState([]) // list of user ids of selected users

  /**
   * Download the user data of the selected users.
   */
  const handleUserDataSelected = () => {
    const url = 'https://api.writingdashboard.xyz/clickapi/getUserData';
    const params = new URLSearchParams();
    // add all selected users user ids to the params list
    for (let index in selectedInstances) {
      params.append("userId", selectedInstances[index]);
    }
    const request = {
      params: params,
      headers: authHeader()
    };
    axios.get(url, request)
      .then((response) => {
        const fileName = response.headers["custom-filename"];
        fileDownload(response.data, fileName);
      })
      .catch(err => {
        console.log(err.response.data)
      })
  }

  /**
   * Download the user data of the user given by the params.
   * @param {event} _event: event data pushed with the call, not required
   * @param {params} params: params of the row where the current user is, of which the userdata needs to be downloaded.
   */
  const handleUserDataSingle = (_event, params) => {
    const url = 'https://api.writingdashboard.xyz/clickapi/getUserData';
    const searchParams = new URLSearchParams();
    // add all selected users user ids to the params list
    searchParams.append("userId", params.row.id)
    const request = {
      params: searchParams,
      headers: authHeader()
    };
    axios.get(url, request)
      .then((response) => {
        const fileName = response.headers["custom-filename"];
        fileDownload(response.data, fileName);
      })
      .catch(err => {
        console.log(err.response.data)
      })
  }

  return (
    <>
      {showDeleteDialog &&
        <AlertDialog title = "Delete user" text = "Are you sure you want to delete this user?"
                     buttonAgree={<Button style={{color: "red"}} onClick={(e) => {deleteUser(deleteId)}}>Yes</Button>}
                     buttonCancel={<Button onClick={(_e) => {setShowDeleteDialog(false)}}>Cancel</Button>}
        />}

    {showFailPopup && <AlertDialog title = "Failure!" 
                        text = {failText}
                        buttonAgree={<Button onClick={(_e) => {setShowFailPopup(false)}}>OK</Button>}
                    />}
      <div style={{ textAlign: 'center', marginBottom: '1vh' }}>
        <BlueButton idStr='downloadUserDataSelectedUsers' onClick={() => {handleUserDataSelected()}}>Download user data of selected users</BlueButton>
      </div>
      <div style={{ height: '80vh' }} >
        <DataGrid
          style={{ maxHeight: '100%' }}
          rows={tableData}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10]}
          checkboxSelection
          onSelectionModelChange={e => setSelectedInstances(e)}
          disableSelectionOnClick
          components={{
            NoRowsOverlay: () => (
              <Stack height="100%" alignItems="center" justifyContent="center">
                No users found!
              </Stack>
            ),
          }}
        />
      </div>
    </>
  );
}

export default Users;