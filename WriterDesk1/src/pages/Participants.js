// materials
import {
  TextField,
  IconButton,
  FormControl,
  InputLabel,
  MenuItem,
  Select, Button, Stack,
} from "@mui/material";
import {
  DeleteOutline,
  Timeline,
} from "@mui/icons-material";
import { DataGrid, GridApi, GridCellValue, GridColDef, GridToolbarContainer } from "@mui/x-data-grid";
import BlueButton from './../components/BlueButton';

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';

// Signup request setup
import axios from 'axios';
import AlertDialog from "../components/AlertDialog";
import { authHeader } from "../helpers/auth-header";

const BASE_URL = "https://localhost:5000/projectapi";



/**
 * 
 * @returns Participants Page
 */



function Participants() {
  const columns: GridColDef[] = [
    {
      field: 'username',
      headerName: 'Username',
      editable: false,
    },
    {
      field: 'password',
      headerName: 'Password',
      editable: false,
    },
    {
      field: 'project',
      headerName: 'Project',
      editable: false,
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

        return <div><IconButton><Timeline /></IconButton><IconButton onClick={(e) => { showDeleteProjectDialog(e, params) }}><DeleteOutline /></IconButton></div>;
      }
    }
  ];

  // replace with list of real projects, needed for project dropdowns

  //set title in parent 'base' 
  const { setTitle } = useOutletContext();

  // initialize participants and projects variables
  const [participants, setParticipants] = useState([]);
  const [projects, setProjects] = useState([]);

  

  useEffect(() => {
    setTitle('Participants');
    getParticpantsAndProjects();
    setProjects([
      { id: 1, projectName: 'test project 1'},
      { id: 2, projectName: 'test project 2'},
      { id: 3, projectName: 'test project 3'},
    ])
  }, []);

  // project in project add
  const [projectAdd, setProjectAdd] = useState('');
  // project in project download
  const [projectDown, setProjectDown] = useState('');

  // dropdown handler for project add
  const handleProjAddPart = (event) => {
    setProjectAdd(event.target.value);
  };
  // dropdown handler for project download
  const handleProjectDownPart = (event) => {
    setProjectDown(event.target.value);
  };

  const [participantCount, setParticipantCount] = useState(0);

  //list of selected items
  const [selectedInstances, setSelectedInstances] = useState([])

  // Perform GET request to retrieve participants of current user from backend
  // Puts response in variable 'participants'
  const getParticpantsAndProjects = () => {
    const url = 'https://127.0.0.1:5000/usersapi/getParticipantsProjects';
    //Perform GET request
    axios.get(url, { headers: authHeader() })
      .then((response) => {
        const projects = response.data
        
        if (projects != null) {
          setProjects(projects);
        }
      })
      .catch(err => {
        console.log('no success')
        console.log(err.response.projects);
      });

  }

  const [showDeleteDialog, setShowDeleteDialog] = useState(false);  // Show dialog when deleting single participant
  const [showDeleteDialogMultiple, setShowDeleteDialogMultiple] = useState(false);  // Show dialog when deleting multiple participants
  const [deleteId, setDeleteId] = useState();  // Id of user that is going to be deleted when pressing delete button

  /*
   * Do POST request containing participantCount and projectAdd variable, receive status of response.
   */
  const handleAddToProject = () => {
    // If input is valid, do post request
    const data = {
      "count": participantCount,
      "projectid": projectAdd,
    }
    const headers = {
      "Content-Type": "application/json"
    }
    axios.post(`${BASE_URL}/addparticipants`, data).then(response => {
      // Post request is successful, participants are registered
      // TODO: reload participant list 
    }).catch(error => {
      // Post request failed, user is not created
      console.error("Something went wrong:", error.response.data);
    });
  };


  /**
    * Delete the participant with the given id from the database. Also delete all corresponding data to the user.
    * @param {event} e: event data pushed with the call, not required
    * @param {number} userId: userId of the participant that needs to be removed.
    */
  const deleteParticipant = (e, userId) => {
    setShowDeleteDialog(false);  // Don't show dialog anymore
    // Url of the server:
    //const url = 'https://127.0.0.1:5000/...'
    // Formdata for the backend call, to which the id has been added:
    //     const formData = new FormData();
    //     formData.append('id', userId);
    //     // Make the call to the backend:
    //     axios.delete(url, { data: formData }).then(response => {
    //         //TODO: Set table data
    //     });

  }


  /**
   * Show the confirmation dialog that asks whether to delete the participant or not
   * @param {event} e: event data pushed with the call, not required
   * @param {params} params: params of the row where the current participant that is removed is in, to be able to remove the correct user.
   */
  const showDeleteProjectDialog = (e, params) => {
    setDeleteId(params.id)  // Set id to be deleted
    setShowDeleteDialog(true);  // Show confirmation dialog
  }

  /**
    * Delete all selected participants from the database. Also delete all corresponding data to the users.
    * @param {event} e: event data pushed with the call, not required
    */
  const deleteSelectedParticipants = (e) => {
    setShowDeleteDialogMultiple(false);  // Don't show dialog anymore
    // // Url of the server:
    // const url = 'https://127.0.0.1:5000/...'
    // // Create a new formdata:
    // const formData = new FormData();
    // // For each of the selected instances, add this id to the formdata:
    // selectedInstances.forEach(id => formData.append('id', id));
    // // Make the backend call:
    // axios.delete(url, { data: formData }).then(response => {
    //     //TODO: Set table data
    // });
  }

  return (
    <>
      {showDeleteDialog &&
        <AlertDialog title="Delete participant" text="Are you sure you want to delete this participant?"
          buttonAgree={<Button onClick={(e) => { deleteParticipant(e, deleteId) }}>Yes</Button>}
          buttonCancel={<Button style={{ color: "red" }} onClick={(e) => { setShowDeleteDialog(false) }}>Cancel</Button>}
        />}
      {showDeleteDialogMultiple &&
        <AlertDialog title="Delete participants" text="Are you sure you want to delete the selected participants?"
          buttonAgree={<Button onClick={(e) => { deleteSelectedParticipants(e) }}>Yes</Button>}
          buttonCancel={<Button style={{ color: "red" }} onClick={(e) => { setShowDeleteDialogMultiple(false) }}>Cancel</Button>}
        />}
      <div style={{ textAlign: 'center', marginBottom: '1vh' }}>
        <TextField
          sx={{ mr: '1vw', verticalAlign: 'middle' }}
          id="noOfParticipants"
          label="Number of participants"
          type="number"
          value={participantCount}
          onChange={(e) => { setParticipantCount(e.target.value) }}
          InputLabelProps={{
            shrink: true,
          }}
        />
        <FormControl sx={{ mr: '1vw', verticalAlign: 'middle', minWidth: 200 }}>
          <InputLabel id="project-add-participants">Project</InputLabel>
          <Select
            labelId="project-add-participants"
            id="project-add-participants"
            value={projectAdd}
            label="Project"
            onChange={handleProjAddPart}
          >
            {projects.map((inst) => <MenuItem key={inst.id} value={inst.id}>{inst.projectName}</MenuItem>)}
          </Select>
        </FormControl>
        <BlueButton idStr='addParticipants' onClick={handleAddToProject}>Add participants</BlueButton>
      </div>
      <div className='topBorder'>
        <FormControl sx={{ mr: '1vw', verticalAlign: 'middle', minWidth: 200 }}>
          <InputLabel id="project-down-participants">Project</InputLabel>
          <Select
            labelId="project-down-participants"
            id="project-down-participants"
            value={projectDown}
            label="Project"
            onChange={handleProjectDownPart}
          >
            {projects.map((inst) => <MenuItem key={inst.id} value={inst.id}>{inst.projectName}</MenuItem>)}
          </Select>
        </FormControl>
        <BlueButton idStr='downloadParticipants' >Download participants</BlueButton>
      </div>
      <div className='topBorder'>
        <BlueButton idStr='downloadSelectedParticipants'>Download selected participants</BlueButton>
        <div style={{ paddingLeft: '2vw', display: 'inline' }} />
        <BlueButton idStr='downloadUserDataSelectedParticipants'>Download user data of selected participants</BlueButton>
      </div>
      <div style={{ justifyContent: 'center', display: 'flex' }}>
        <div style={{ height: '80vh', maxHeight: '400px', width: '50vw' }} >
          <DataGrid
            rows={participants} /* TODO, changed from rows to participants */
            columns={columns} /* TODO */
            pageSize={5}
            rowsPerPageOptions={[5]}
            checkboxSelection
            onSelectionModelChange={e => setSelectedInstances(e)}
            disableSelectionOnClick
            components={{
              NoRowsOverlay: () => (
                <Stack height="100%" alignItems="center" justifyContent="center">
                  No participants to show
                </Stack>
              ),
              Toolbar: () => (
                <GridToolbarContainer>
                  <IconButton onClick={(e) => { setShowDeleteDialogMultiple(true) }}><DeleteOutline /></IconButton>
                </GridToolbarContainer>
              )
            }}
          />
        </div>
      </div>
    </>
  );
}

export default Participants;