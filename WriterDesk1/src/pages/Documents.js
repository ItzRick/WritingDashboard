// materials
import {
  IconButton, 
  Stack,
} from "@mui/material";
import {
  DeleteOutline,
  Grading,
  Refresh,
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
 * @returns Documents Page
 */
const Documents = () => {
  // State to keep track of the data inside the table:
  const [tableData, setTableData] = useState([])

  // State to keep track of the IDs of the instances that are currently selected:
  const [selectedInstances, setSelectedInstances] = useState([])

  //set title in parent 'base': 
  const { setTitle } = useOutletContext();
  useEffect(() => {
    setTitle('Documents');
  });

  //   Name of the columns as set inside the datagrid:
  const columns = [
    {
      field: 'filename',
      headerName: 'Filename',
      editable: false,
      flex: 1,
      minWidth: 250
    },
    {
      field: 'fileType',
      headerName: 'FileType',
      editable: false,
      flex: 1
    },
    {
      field: 'courseCode',
      headerName: 'Course',
      editable: false,
      flex: 1
    },
    {
      field: 'scoreStyle',
      headerName: 'h1',
      type: "number",
      editable: false,
      flex: 1
    },
    {
      field: 'scoreCohesion',
      headerName: 'h2',
      type: "number",
      editable: false,
      flex: 1
    },
    {
      field: 'scoreStructure',
      headerName: 'h3',
      type: "number",
      editable: false,
      flex: 1
    },
    {
      field: 'scoreIntegration',
      headerName: 'h4',
      type: "number",
      editable: false,
      flex: 1
    },
    {
      field: 'date',
      headerName: 'Date ',
      editable: false,
      flex: 1
    },
    {
      field: "actions",
      headerName: "Actions",
      sortable: false,
      flex: 1,
      renderCell: (params) => {
        return <div><IconButton><Grading /></IconButton><IconButton onClick={(e) => { deleteFile(e, params) }}  ><DeleteOutline /></IconButton></div>;
      }
    }
  ];


  /**
 * Remove the file with the ID as required from the server.
 * 
 * @param {event} _event: event data pushed with the call, not required
 * @param {params} params: params of the row where the current file that is removed is in, to be able to remove the correct file.
 */
  const deleteFile = (_event, params) => {
    //   Url of the server:
    const url = 'https://127.0.0.1:5000/fileapi/filedelete'
    // Formdata for the backend call, to which the id has been added:
    const formData = new FormData();
    formData.append('id', params.id);
    // Make the call to the backend:
    axios.delete(url, { data: formData })
      .then(() => { setData() });
  }

  /**
  * Remove the files with the IDs that are selected in selectedInstances from the server.
  * 
  */
  const deleteAllFiles = () => {
    // Url of the server:
    const url = 'https://127.0.0.1:5000/fileapi/filedelete'
    // Create a new formdata:
    const formData = new FormData();
    // For each of the selected instances, add this id to the formdata:
    selectedInstances.forEach(id => formData.append('id', id));
    // Make the backend call:
    axios.delete(url, { data: formData })
      .then(() => { setData() });
  }
  /**
   * Make the backend call, to et the data in the tableData state.
   * 
   */
  const setData = () => {
    //   The backend url:
    const url = 'https://127.0.0.1:5000/fileapi/fileretrieve';
    // The parameters, sortingAttribute and userId need to be changed later:
    const params = {
      userId: 123,
      sortingAttribute: '',
    }
    // Make the backend call and set the table data from the response data:
    axios.get(url, { params })
      .then((response) => {
        setTableData(response.data)
      })
  }

  useEffect(() => {
    setData();
  }, []);

  return (
    <DataGrid
      style={{ maxHeight: '100%'}}
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
            No documents uploaded, please upload a document!
          </Stack>
        ),
        Toolbar: () => (
          <GridToolbarContainer>
            <IconButton onClick={deleteAllFiles} ><DeleteOutline /></IconButton>
            <IconButton onClick={setData} ><Refresh /></IconButton>
          </GridToolbarContainer>
        )
      }}
    />
  );
}

export default Documents;