// materials
import {
  Button,
  IconButton,
  Stack,
  Tooltip,
} from "@mui/material";
import {
  DeleteOutline,
  Grading,
  Refresh,
  Cached
} from "@mui/icons-material";
import { DataGrid, GridToolbarContainer } from "@mui/x-data-grid";

// routing
import { useOutletContext, useNavigate, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';


import React from 'react';
import "../css/styles.css";
import "../css/main.css";

import AlertDialog from "../components/AlertDialog";
import {authHeader} from "../helpers/auth-header";


/**
 * 
 * @returns Documents Page
 */
const ParticipantDocuments = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // State to keep track of the data inside the table:
  const [tableData, setTableData] = useState([])

  // State to keep track of the IDs of the instances that are currently selected:
  const [selectedInstances, setSelectedInstances] = useState([])

  const [showDeleteDialog, setShowDeleteDialog] = useState(false);  // Show dialog when deleting single file
  const [showDeleteDialogMultiple, setShowDeleteDialogMultiple] = useState(false);  // Show dialog when deleting multiple files

  const [deleteId, setDeleteId] = useState();  // ID of file that is going to be deleted when pressing delete button

  //set title in parent 'base': 
  const { setTitle } = useOutletContext();
  useEffect(() => {
    setTitle('Documents of Participant');
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
      headerName: 'Language and Style score',
      type: "number",
      editable: false,
      flex: 1
    },
    {
      field: 'scoreCohesion',
      headerName: 'Cohesion score',
      type: "number",
      editable: false,
      flex: 1
    },
    {
      field: 'scoreStructure',
      headerName: 'Structure score',
      type: "number",
      editable: false,
      flex: 1
    },
    {
      field: 'scoreIntegration',
      headerName: 'Source Integration and Content score',
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
        // actions
        return <div>
          <Tooltip title="View the feedback of this document.">
            <IconButton id={'navigate' + params.row.filename} onClick={(e) => { navigateToDoc(e, params) }} ><Grading /></IconButton>
          </Tooltip>
          <Tooltip title="Delete this document.">
            <IconButton id={'delete' + params.row.filename} onClick={(e) => { showDeleteFileDialog(e, params) }}  ><DeleteOutline /></IconButton>
          </Tooltip>
        </div>;
      }
    }
  ];


  /**
   * Navigate to the Document page and add the file id as state parameter.
   * @param {event} _event: event data pushed with the call, not required
   * @param {params} params: params of the row where the current file is that needs to be navigated to.
   */
  const navigateToDoc = (_event, params) => {
    navigate('/Document', { state: { fileId: params.id, fileName: params.row.filename } });
  }

  /**
   * Show the confirmation dialog that asks whether to delete the file or not
   * @param {event} e: event data pushed with the call, not required
   * @param {params} params: params of the row where the current file that is removed is in, to be able to remove the correct file.
   */
  const showDeleteFileDialog = (e, params) => {
    setDeleteId(params.id)  // Set id to be deleted
    setShowDeleteDialog(true);  // Show confirmation dialog
  }


  /**
 * Remove the file with the ID as required from the server.
 * 
 * @param {event} _event: event data pushed with the call, not required
 * @param {number} fileId: fileId of the current file that is removed.
 */
  const deleteFile = (_event, fileId) => {
    setShowDeleteDialog(false);  // Don't show dialog anymore

    //   Url of the server:
    const url = '/api/fileapi/filedelete'
    // Formdata for the backend call, to which the id has been added:
    const formData = new FormData();
    formData.append('id', fileId);
    // Make the call to the backend:
    axios.delete(url, { data: formData })
      .then(() => { setData() 
    });
  }

  /**
  * Remove the files with the IDs that are selected in selectedInstances from the server.
  * 
  */
  const deleteAllFiles = () => {
    setShowDeleteDialogMultiple(false);  // Don't show confirmation dialog anymore

    // Url of the server:
    const url = '/api/fileapi/filedelete'
    // Create a new formdata:
    const formData = new FormData();
    // For each of the selected instances, add this id to the formdata:
    selectedInstances.forEach(id => formData.append('id', id));
    // Make the backend call:
    axios.delete(url, { data: formData })
      .then(() => { setData() });
  }

  /**
  * Re generate the feedback for the files which are selected, so which are in selectedInstances.
  * 
  */
  const generateFeedback = () => {
    let params = new URLSearchParams();
    selectedInstances.forEach(id => params.append("fileId", id));
    let generateUrl = '/api/feedback/generate';
    const config = {
      params: params,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }
    axios.post(generateUrl, {}, config)
      .catch((error) => {
        console.log(error.response.data);
      });
  }

  /**
   * Make the backend call, to et the data in the tableData state.
   * 
   */
  const setData = () => {
    //   The backend url:
    const url = '/api/fileapi/fileretrieve';
    // id of current user
    const userId = location.state.userId;
    // The parameter, sortingAttribute need to be changed later:
    const params = {
      userId: userId,
      sortingAttribute: '',
    }
    // Make the backend call and set the table data from the response data:
    axios.get(url, { params, headers: authHeader()})
      .then((response) => {
        setTableData(response.data)
      })
  }

  useEffect(() => {
    setData();
  }, []);

  return (
    <>
      {showDeleteDialog &&
        <AlertDialog title="Delete file" text="Are you sure you want to delete this file?"
          buttonAgree={<Button id='agree' style={{ color: "red" }} onClick={(e) => { deleteFile(e, deleteId) }}>Yes</Button>}
          buttonCancel={<Button id='disagree' onClick={(e) => { setShowDeleteDialog(false) }}>Cancel</Button>}
        />}
      {showDeleteDialogMultiple &&
        <AlertDialog title="Delete files" text="Are you sure you want to delete the selected files?"
          buttonAgree={<Button id='agree' style={{ color: "red" }} onClick={(e) => { deleteAllFiles() }}>Yes</Button>}
          buttonCancel={<Button id='disagree' onClick={(e) => { setShowDeleteDialogMultiple(false) }}>Cancel</Button>}
        />}
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
              No documents uploaded, please upload a document!
            </Stack>
          ),
          Toolbar: () => (
            <GridToolbarContainer>
              <Tooltip title="Delete selected documents.">
                <IconButton onClick={(e) => {setShowDeleteDialogMultiple(true)}}><DeleteOutline /></IconButton>
              </Tooltip>
              <Tooltip title="Refresh the documents overview.">
                <IconButton onClick={setData} ><Refresh /></IconButton>
              </Tooltip>
              <Tooltip title="Regenerate feedback for selected files.">
                <IconButton onClick={generateFeedback} ><Cached /></IconButton>
              </Tooltip>
            </GridToolbarContainer >
          )
        }}
/>
    </>
  );
}

export default ParticipantDocuments;