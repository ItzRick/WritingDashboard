import {
    TextField,
    IconButton,
    Stack,
    FormControl,
    InputLabel,
    MenuItem,
    Select,
} from "@mui/material";
import {
    DeleteOutline,
    Storage,
    PersonSearch,
} from "@mui/icons-material";
import { DataGrid, GridToolbarContainer } from "@mui/x-data-grid";
import BlueButton from './../components/BlueButton';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';


// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from "axios";

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

    // TODO replace with real projects
    const projects = [{
        id: '0',
        projectName: 'toyProject',
        partCount: '12'
    },
    {
        id: '1',
        projectName: 'toyProject2',
        partCount: '120'
    }

    ]

    // upon first render, set the table data
    useEffect(() => {
        // TODO: replace table data with real data
        setTableData(projects);
    }, []);


    //data displayed in the table
    const [tableData, setTableData] = useState([])
    //list of selected items
    const [selectedInstances, setSelectedInstances] = useState([])
    // project selected in download user data
    const [projectDown, setProjectDown] = useState('');

    // dropdown handler for project add
    const handleProjDown = (event) => {
        setProjectDown(event.target.value);
    };

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
                    <IconButton onClick={(e) => { deleteProject(e, params) }}  ><DeleteOutline /></IconButton>
                </div>);
            }
        }
    ];

    // start date of project
    const [startData, setStartData] = useState(new Date());
    // end date of project
    const [endData, setEndData] = useState(new Date());

    const [projectName, setProjectName] = useState();
    const [numberOfParticipants, setNumberOfParticipants] = useState();

     /**
      * Create a research project in the database. Also generate accounts for the participants based on the given input.
      * @param {event} e: event data pushed with the call, not required
      */
    const createProject = (e) => {
        // Check if the number of participants is valid
        if (!(numberOfParticipants !== '' && numberOfParticipants >= 0 && numberOfParticipants <= 10000)) {
            alert('Make sure the number of participants is a valid number between 0 and 10000');
            return null;
        }
        let userId = 1; //TODO: Change to current userId

        const formData = new FormData();
        formData.append('userId', userId);  // Add userId to form
        formData.append('projectName', projectName);  // Add input name to form

        // Create project request
        axios.post(`https://localhost:5000/projectapi/setProject`, formData).then(response => {
            const data = {
                "count": numberOfParticipants,
                "projectid": 1, //TODO: Change projectId
            }
            // Add participants request
            axios.post(`https://localhost:5000/projectapi/addparticipants`, data).then(response => {
                //TODO: Set table data
            });
        });


    }

    /**
      * Delete the research project with the given id from the database. Also delete all corresponding data to the project.
      * @param {event} e: event data pushed with the call, not required
      * @param {params} params: params of the row where the current project that is removed is in, to be able to remove the correct project.
      */
    const deleteProject = (e, params) => {
        // Url of the server:
        const url = 'https://127.0.0.1:5000/projectapi/deleteProject'
        // Formdata for the backend call, to which the id has been added:
        const formData = new FormData();
        formData.append('projectId', params.id);
        // Make the call to the backend:
        axios.delete(url, { data: formData }).then(response => {
            //TODO: Set table data
        });
    }

    /**
      * Delete all selected research project from the database. Also delete all corresponding data to the projects.
      * @param {event} e: event data pushed with the call, not required
      */
    const deleteSelectedProjects = (e) => {
        // Url of the server:
        const url = 'https://127.0.0.1:5000/projectapi/deleteProject'
        // Create a new formdata:
        const formData = new FormData();
        // For each of the selected instances, add this id to the formdata:
        selectedInstances.forEach(id => formData.append('projectId', id));
        // Make the backend call:
        axios.delete(url, { data: formData }).then(response => {
            //TODO: Set table data
        });
    }


    return (
        <>
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
                    {/* downloading user data */}
                    {/* Select start data */}
                    <LocalizationProvider dateAdapter={AdapterDayjs} sx={{ margin: '1vh', verticalAlign: 'middle' }}>
                        <DatePicker
                            sx={{ margin: '1vh', verticalAlign: 'middle' }}
                            label="Start date"
                            openTo="day"
                            views={['year', 'month', 'day']}
                            value={startData}
                            onChange={(newDate) => {
                                setStartData(newDate);
                            }}
                            renderInput={(params) => <TextField sx={{ margin: '1vh', verticalAlign: 'middle' }} {...params} />}
                        />
                    </LocalizationProvider>
                    {/* Select end date */}
                    <LocalizationProvider dateAdapter={AdapterDayjs} sx={{ margin: '1vh', verticalAlign: 'middle' }}>
                        <DatePicker
                            sx={{ margin: '1vh', verticalAlign: 'middle' }}
                            label="End date"
                            openTo="day"
                            views={['year', 'month', 'day']}
                            value={endData}
                            onChange={(newDate) => {
                                setEndData(newDate);
                            }}
                            renderInput={(params) => <TextField sx={{ margin: '1vh', verticalAlign: 'middle' }} {...params} />}
                        />
                    </LocalizationProvider>
                    {/* Project Dropdown */}
                    <FormControl sx={{ mr: '1vw', verticalAlign: 'middle', minWidth: 200 }}>
                    <InputLabel id="project-down-participants">Project</InputLabel>
                    <Select
                        labelId="project-down-participants-label"
                        id="project-down-participants"
                        value={projectDown}
                        label="Project"
                        onChange={handleProjDown}
                    >
                        {projects.map((inst) => <MenuItem value={inst.id}>{inst.projectName}</MenuItem>)}
                    </Select>
                </FormControl>
                <BlueButton idStr='downloadUserData' style={{ margin: '1vh', verticalAlign: 'middle' }}>Download user data</BlueButton>
            </div>
            <div className="topBorder">
                {/* downloading participants and user data */}<BlueButton idStr='downloadParticipants' >Download participants of selected projects</BlueButton>
                <div style={{ paddingLeft: '2vw', display: 'inline' }} />
                <BlueButton idStr='downloadUserDataForSelectedProject' >Download user data of participants of selected project</BlueButton>
            </div>
            {/* displaying projects */}
            <div style={{ justifyContent: 'center', display: 'flex' }}>
                <div style={{ height: '80vh', maxHeight: '400px', width: '50vw' }} >
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
                                    <IconButton onClick={(e) => {deleteSelectedProjects(e)}}><DeleteOutline /></IconButton>
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