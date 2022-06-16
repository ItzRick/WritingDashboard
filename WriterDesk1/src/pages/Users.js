import { useOutletContext } from 'react-router-dom';
import { useState, useEffect } from 'react';
import {DataGrid, GridApi, GridCellValue, GridColDef} from "@mui/x-data-grid";
import IconButton from "@mui/material/IconButton";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";

import RoleDialog from "./../components/RoleDialog";


/**
 * 
 * @returns Users Page
 */

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
      const userId = params.id;
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
      const onClick = (e) => {
        e.stopPropagation(); // don't select this row after clicking

        const api: GridApi = params.api;
        const thisRow: Record<string, GridCellValue> = {};

        api
          .getAllColumns()
          .filter((c) => c.field !== "__check__" && !!c)
          .forEach(
            (c) => (thisRow[c.field] = params.getValue(params.id, c.field))
          );

        return alert(JSON.stringify(thisRow, null, 4));
      };

      return <div><IconButton><DeleteOutlineIcon /></IconButton></div>;
    }
  }
];

const rows = [
  {id: 1, username: 'Bob', role: 'Researcher'},
  {id: 2, username: 'Alice', role: 'Researcher'},
  {id: 3, username: 'Felix', role: 'Student'},
  {id: 4, username: 'Patrick', role: 'Student'},
  {id: 5, username: 'Carla', role: 'Researcher'},
];

const Users = () => {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Users');
    });

    return (
        <>
            <div style={{height: '80vh', maxHeight: '400px'}} >
                <DataGrid
                  rows={rows}
                  columns={columns}
                  pageSize={5}
                  rowsPerPageOptions={[5]}
                  checkboxSelection
                  disableSelectionOnClick
                />
            </div>
        </>
    );
}

export default Users;