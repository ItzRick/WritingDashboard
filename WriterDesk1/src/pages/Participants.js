// materials
import {
  TextField,
  IconButton,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Button,
  Stack
} from "@mui/material";
import {
  FormatAlignJustify,
  DeleteOutline,
} from "@mui/icons-material";
import { DataGrid, GridColDef, GridToolbarContainer } from "@mui/x-data-grid";
import BlueButton from './../components/BlueButton';

// routing
import { useOutletContext, Link, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

// Signup request setup
import axios from 'axios';
import AlertDialog from "../components/AlertDialog";
import { authHeader } from "../helpers/auth-header";

import fileDownload from 'js-file-download';

const BASE_URL = "https://api.writingdashboard.xyz/projectapi";


/**
 *
 * @returns Participants Page
 */
const Participants = () => {
  const navigate = useNavigate();

  const columns = [
    {
      field: 'username',
      headerName: 'Username',
      editable: false,
      flex: 1,
    },
    {
      field: 'projectid',
      headerName: 'Project ID',
      editable: false,
    },
    {
      field: 'projectname',
      headerName: 'Project',
      editable: false,
    },
    {
      field: "actions",
      headerName: "Actions",
      sortable: false,
      renderCell: (params) => {
        // action buttons
        return (<div>
          <Tooltip title="View the documents of this participant.">
            <IconButton onClick={(e) => { navigateToPartDoc(e, params) }} ><FormatAlignJustify /></IconButton>
          </Tooltip>
          <Tooltip title="Delete this participant.">
            <IconButton onClick={(e) => { showdeleteProjectDialog(e, params) }}><DeleteOutline /></IconButton>
          </Tooltip>
          </div>);
      }
    }
  ];
  //set title in parent 'base'
  const { setTitle } = useOutletContext();

  /**
   * Navigate to the ParticipantDocuments page and add the user id as state parameter.
   * @param {event} _event: event data pushed with the call, not required
   * @param {params} params: params of the row where the current user is that needs to be navigated to.
   */
  const navigateToPartDoc = (_event, params) => {
    navigate('/ParticipantDocuments', { state: { userId: params.id } });
  }

  // initialize participants and projects states
  const [participants, setParticipants] = useState([]);
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    setTitle('Participants');
    getParticpantsAndProjects();
  }, []);

  // project in project add
  const [projectAdd, setProjectAdd] = useState('');

  // dropdown handler for project add
  const handleProjAddPart = (event) => {
    setProjectAdd(event.target.value);
  };
  /*
   * Do POST request containing participantCount and projectAdd variable, recieve status of response.
   * When successful, download response csv file.
   */
  const handleAddToProject = () => {
    // If input is valid, do post request
    const data = {
      "nrOfParticipants": participantCount,
      "projectid": projectAdd,
    }
    const headers = {
      "Content-Type": "application/json"
    }
    axios.post(`${BASE_URL}/addParticipants`, data, { headers: authHeader() }).then(response => {
      // Post request is successful, participants are registered
      // TODO: reload participant list 
      const fileName = response.headers["custom-filename"];
      fileDownload(response.data, fileName);
    }).catch(error => {
      // Post request failed, user is not created
      console.error("Something went wrong:", error.response.data);
    });
  };

  const [selectedInstances, setSelectedInstances] = useState([]) // list of user ids of selected participants

  /**
   * Perform GET request to retrieve csv file containing user data of selected
   * participants.
   */
  const handleUserDataParticipants = () => {
    const url = 'https://api.writingdashboard.xyz/clickapi/getParticipantsUserData';
    const params = new URLSearchParams();
    // add all selected participant user ids to the params list
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
  const [participantCount, setParticipantCount] = useState(0);

  /**
   * Perform GET request to retrieve participants of current user from backend
   * Puts response in variable 'participants'
   */
  const getParticpantsAndProjects = () => {
    const url = 'https://api.writingdashboard.xyz/usersapi/getParticipantsProjects';
    //Perform GET request
    axios.get(url, { headers: authHeader() })
      .then((response) => {
        const resp = response.data
        if (resp != null) {
          setParticipants(resp);

          // get all unique project ids
          const result = []; //result
          const map = new Map(); //store all ids here
          for (const item of resp) {
            if (!map.has(item.projectid)) {
              map.set(item.projectid, true);    // set any value to Map
              // add to result
              result.push({
                projectid: item.projectid,
                projectname: item.projectname
              });
            }
          }
          // put unique id and name into state projects
          setProjects(result);
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


  /**
    * Delete the participant with the given id from the database. Also delete all corresponding data to the user.
    * @param {event} e: event data pushed with the call, not required
    * @param {number} userId: userId of the participant that needs to be removed.
    */
  const deleteParticipant = (e, userId) => {
    setShowDeleteDialog(false);  // Don't show dialog anymore
    // TODO: future feature for Bas or Jordy
    // Url of the server:
    const url = 'https://api.writingdashboard.xyz/usersapi/deleteUserResearcher'
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
  const showdeleteProjectDialog = (e, params) => {
    setDeleteId(params.id)  // Set id to be deleted
    setShowDeleteDialog(true);  // Show confirmation dialog
  }

  /**
    * Delete all selected participants from the database. Also delete all corresponding data to the users.
    * @param {event} e: event data pushed with the call, not required
    */
  const deleteSelectedParticipants = (e) => {
    setShowDeleteDialogMultiple(false);  // Don't show dialog anymore
    // TODO: future feature for Bas or Jordy
    // // Url of the server:
    const url = 'https://api.writingdashboard.xyz/usersapi/deleteUserResearcher'
    // Create a new formdata:
    const formData = new FormData();
    // For each of the selected instances, add this id to the formdata:
    selectedInstances.forEach(id => {
      const data = {
          "userID": id
      }
      axios.post(url, data, {headers: authHeader()}).then(r => {getParticpantsAndProjects()})
    });

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
          inputProps={{
            min: 0,
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
            {projects.map((inst) => <MenuItem key={inst.projectid} value={inst.projectid}>{inst.projectname}, {inst.projectid}</MenuItem>)}
          </Select>
        </FormControl>
        <BlueButton idStr='addParticipants' onClick={handleAddToProject}>Add participants</BlueButton>
      </div>
      <div className='topBorder'>
        <div style={{ paddingLeft: '2vw', display: 'inline' }} />
        <BlueButton idStr='downloadUserDataSelectedParticipants' onClick={handleUserDataParticipants}>Download user data of selected participants</BlueButton>
      </div>
      <div style={{ justifyContent: 'center', display: 'flex' }}>
        <div style={{ height: '80vh', maxHeight: '400px', width: '50vw' }} >
          <DataGrid
            rows={participants}
            columns={columns}
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