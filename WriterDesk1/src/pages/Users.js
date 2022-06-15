// materials
import {
  IconButton,
  Stack,
} from "@mui/material";
import {
  DeleteOutline,
  PersonOutline,
} from "@mui/icons-material";
import { DataGrid, GridToolbarContainer } from "@mui/x-data-grid";

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';


import React from 'react';
import "../css/styles.css";
import "../css/main.css";

/**
 * 
 * @returns Users Page
 */

const Users = () => {

  // State to keep track of the data inside the table:
  const [tableData, setTableData] = useState([])

    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Users');
    });

    const columns = [
    {
      field: 'username',
      headerName: 'Username',
      editable: false,
      flex: 1,
      minWidth: 250
    },
    {
      field: 'role',
      headerName: 'Role',
      editable: false,
      flex: 1
    },
    {
      field: "actions",
      headerName: "Actions",
      sortable: false,
      flex: 1,

        renderCell: (params) => {
          return <div><IconButton><PersonOutline /></IconButton><IconButton><DeleteOutline /></IconButton></div>;
        }
    }
    ];

  const setData = () => {
    //   The backend url:
    const url = 'https://127.0.0.1:5000/usersapi/users';
    // Make the backend call and set the table data from the response data:
    axios.get(url)
      .then((response) => {
        setTableData(response.data)
      })
  }

  useEffect(() => {
    setData();
  }, []);

    return (
        <>
            <div style={{height: '80vh', maxHeight: '400px'}} >
                <DataGrid
      style={{ maxHeight: '100%'}}
      rows={tableData}
      columns={columns}
      pageSize={15}
      rowsPerPageOptions={[15]}
      checkboxSelection
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