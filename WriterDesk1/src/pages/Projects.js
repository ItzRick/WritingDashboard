import {
    TextField,
    IconButton,
    Stack,
    Button,
} from "@mui/material";
import {
    DeleteOutline,
    Storage,
    PersonSearch,
} from "@mui/icons-material";
import { DataGrid, GridToolbarContainer } from "@mui/x-data-grid";
import BlueButton from './../components/BlueButton';
import AlertDialog from "../components/AlertDialog";
import fileDownload from 'js-file-download';

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from "axios";

// User authentication
import {authHeader} from "../helpers/auth-header";

/**
 *
 * @returns Projects Page
 */
const Projects = () => {
    // set title in parent 'base'
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Projects');
    });

    /**
     * retrieve projects
     * @param {*} e 
     * @param {*} projId 
     */
    const setProjects = () => {

        // Delete project from all tables in database and delete files from the server:
        axios.get('https://127.0.0.1:5000/projectapi/viewProjectsOfUser', {headers:authHeader()} ).then(response => {
            //TODO: Set table data
            console.log(response.data)
            setTableData(response.data);
        });
    }

    // upon first render, set the table data
    useEffect(() => {
        // TODO: replace table data with real data
        setProjects()
    }, []);


    //data displayed in the table
    const [tableData, setTableData] = useState([])
    //list of selected items
    const [selectedInstances, setSelectedInstances] = useState([])

    // columns in data-grid
    const columns = [
        {
            field: 'projectName',
            headerName: 'Project name',
            editable: false,
            flex: 1,
            minWidth: 250
        },
        {
            field: 'partCount',
            headerName: 'Nr. of participants',
            editable: false,
            flex: 1
        },
        {
            field: "actions",
            headerName: "Actions",
            sortable: false,
            flex: 1,
            renderCell: (params) => {
                return (<div>
                    <IconButton onClick={(e) => { }}  ><PersonSearch /></IconButton>
                    <IconButton onClick={(e) => { }}  ><Storage /></IconButton>
                    <IconButton onClick={(e) => { showdeleteProjectDialog(e, params) }}  ><DeleteOutline /></IconButton>
                </div>);
            }
        }
    ];

    const [projectName, setProjectName] = useState();  // Project name for project to be created
    const [numberOfParticipants, setNumberOfParticipants] = useState();  // Number of participants for project to be created

    const [showDeleteDialog, setShowDeleteDialog] = useState(false);  // Show dialog when deleting single project
    const [showDeleteDialogMultiple, setShowDeleteDialogMultiple] = useState(false);  // Show dialog when deleting multiple projects
    const [showNrOfParticipantsDialog, setShowNrOfParticipantsDialog] = useState(false);  // Show dialog when trying to add invalid number of participants

    const [deleteId, setDeleteId] = useState();  // Id that is going to be deleted when pressing delete button

     /**
      * Create a research project in the database. Also generate accounts for the participants based on the given input.
      * @param {event} e: event data pushed with the call, not required
      */
    const createProject = (e) => {
        // Check if the number of participants is valid
        if (!(numberOfParticipants !== '' && numberOfParticipants >= 0 && numberOfParticipants <= 1000)) {
            setShowNrOfParticipantsDialog(true);
            return null;
        }

        const formData = new FormData();
        formData.append('projectName', projectName);  // Add input name to form
        // Create project request
        axios.post(`https://localhost:5000/projectapi/setProject`, formData, {headers: authHeader()}).then(response => {
            const data = {
                "nrOfParticipants": numberOfParticipants,  // Add input of numberOfParticipants
                "projectid": response.data,  // Get project id from response
            }
            // Add participants request
            axios.post(`https://localhost:5000/projectapi/addParticipants`, data, {headers: authHeader()}).then(response => {
                const fileName = response.headers["custom-filename"];
                fileDownload(response.data, fileName);
                setProjects()
            });
        });
    }

    /**
      * Delete the research project with the given id from the database. Also delete all corresponding data to the project.
      * @param {event} e: event data pushed with the call, not required
      * @param {number} projId: projid of the project that needs to be removed.
      */
    const deleteProject = (e, projId) => {
        setShowDeleteDialog(false);  // Don't show dialog anymore

        // Formdata for the project id to be added:
        const formData = new FormData();
        formData.append('projectId', projId);

        const headers = authHeader() // Authentication header of current user

        // Delete project from all tables in database and delete files from the server:
        axios.delete('https://127.0.0.1:5000/projectapi/deleteProject',  {headers, data: formData} ).then(response => {
            setProjects()
        });
    }

    /**
     * Show the confirmation dialog that asks whether to delete the project or not
     * @param {event} e: event data pushed with the call, not required
     * @param {params} params: params of the row where the current project that is removed is in, to be able to remove the correct project.
     */
    const showdeleteProjectDialog = (e, params) => {
        setDeleteId(params.id)  // Set id to be deleted
        setShowDeleteDialog(true);  // Show confirmation dialog
    }


    /**
      * Delete all selected research project from the database. Also delete all corresponding data to the projects.
      * @param {event} e: event data pushed with the call, not required
      */
    const deleteSelectedProjects = (e) => {
        setShowDeleteDialogMultiple(false);  // Don't show confirmation dialog anymore

        // Create a new formdata:
        const formData = new FormData();
        // For each of the selected instances, add this id to the formdata:
        selectedInstances.forEach(id => formData.append('projectId', id));

        const headers = authHeader() // Authentication header of current user

        // Delete projects from all tables in database and delete files from the server:
        axios.delete('https://127.0.0.1:5000/projectapi/deleteProject', {headers, data: formData }).then(response => {
            setProjects()
        });
    }

    return (
        <>
            {showDeleteDialog &&
              <AlertDialog title = "Delete project" text = "Are you sure you want to delete this project?"
                           buttonAgree={<Button style={{color: "red"}} onClick={(e) => {deleteProject(e, deleteId)}}>Yes</Button>}
                           buttonCancel={<Button onClick={(e) => {setShowDeleteDialog(false)}}>Cancel</Button>}
              />}
            {showDeleteDialogMultiple &&
              <AlertDialog title = "Delete projects" text = "Are you sure you want to delete the selected projects?"
                           buttonAgree={<Button style={{color: "red"}} onClick={(e) => {deleteSelectedProjects(e)}}>Yes</Button>}
                           buttonCancel={<Button onClick={(e) => {setShowDeleteDialogMultiple(false)}}>Cancel</Button>}
              />}
            {showNrOfParticipantsDialog &&
              <AlertDialog title = "Number of participants" text = "Make sure the number of participants is a valid number between 0 and 1000!"
                           buttonAgree={<Button onClick={(e) => {setShowNrOfParticipantsDialog(false)}}>Ok</Button>}
              />}

                {/* adding projects */}
                <div style={{ textAlign: 'center', marginBottom: '1vh' }}>
                    <TextField
                        sx={{ mr: '1vw', verticalAlign: 'middle' }}
                        id="projectName"
                        label={"Project name"}
                        inputProps={{ maxLength: 256 }}
                        onChange={(e) => setProjectName(e.target.value)}
                    />
                    <TextField
                        sx={{ mr: '1vw', verticalAlign: 'middle' }}
                        id="partCount"
                        type='number'
                        label={"Number of Participants"}
                        InputProps={{ inputProps: { min: 0 } }}
                        onChange={(e) => setNumberOfParticipants(e.target.value)}
                    />
                    <BlueButton idStr='addProject' style={{ verticalAlign: 'middle' }} onClick={(e) => {createProject(e)}}>Add project</BlueButton>
                </div>
                <div />
            <div className="topBorder">
            </div>
            {/* displaying projects */}
            <div style={{ justifyContent: 'center', display: 'flex' }}>
                <div style={{ height: '80vh', minHeight: '400px', width: '70vw' }} >
                    <DataGrid
                        style={{ height: '70%' }}
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
                                    No projects created, please create a project!
                                </Stack>
                            ),
                            Toolbar: () => (
                                <GridToolbarContainer>
                                    <IconButton onClick={(e) => {setShowDeleteDialogMultiple(true)}}><DeleteOutline /></IconButton>
                                </GridToolbarContainer>
                            )
                        }}
                    />
                </div>
            </div>
        </>
    );
}




export default Projects;