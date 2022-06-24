// materials
import {
  IconButton,
  Stack,
  Tooltip,
} from "@mui/material";
import {
  DeleteOutline,
} from "@mui/icons-material";

// routing
import { useOutletContext } from 'react-router-dom';
import axios from 'axios';
import { useState, useEffect } from 'react';
import { DataGrid, GridColDef } from "@mui/x-data-grid";

import RoleDialog from "./../components/RoleDialog";
import BlueButton from './../components/BlueButton';

import React from 'react';
import "../css/styles.css";
import "../css/main.css";
import { authHeader } from "../helpers/auth-header";
import fileDownload from 'js-file-download';

/**
 * 
 * @returns Users Page
 */
const Users = () => {

  function deleteUser(userID) {
        //   The backend url:
        const url = 'https://127.0.0.1:5000/usersapi/deleteUserAdmin';
        // Make the backend call and set the table data from the response data:
        axios.post(url,{userID: userID},{headers: authHeader()}).then((response) => {
        })
        window.location.reload();
        return false;
  }

  // State to keep track of the data inside the table:
  const [tableData, setTableData] = useState([])

  const columns: GridColDef[] = [
    {
      field: 'username',
      headerName: 'Username',
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
          <Tooltip title="Delete this user.">
            <IconButton onClick={(e) => { deleteUser(params.row.id) }}><DeleteOutline /></IconButton>
          </Tooltip>
        </div>);
      }
    }
  ];

  const setData = () => {
    //   The backend url:
    const url = 'https://127.0.0.1:5000/usersapi/users';
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

  const handleUserData = () => {
    const url = 'https://127.0.0.1:5000/clickapi/getUserData';
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

  return (
    <>
      <BlueButton idStr='downloadUserData' onClick={() => {handleUserData()}}>Download user data</BlueButton>
      <div style={{ height: '80vh', maxHeight: '400px' }} >
        <DataGrid
          style={{ maxHeight: '100%' }}
          rows={tableData}
          columns={columns}
          pageSize={15}
          rowsPerPageOptions={[15]}
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