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
                    <IconButton onClick={(e) => { }}  ><DeleteOutline /></IconButton>
                </div>);
            }
        }
    ];

    // start date of project
    const [startData, setStartData] = useState(new Date());
    // end date of project
    const [endData, setEndData] = useState(new Date());

    return (
        <>
            {/* adding projects */}
            <div style={{ textAlign: 'center', marginBottom: '1vh' }}>
                <TextField
                    sx={{ mr: '1vw', verticalAlign: 'middle' }}
                    id="projectName"
                    label={"Project name"}
                />
                <TextField
                    sx={{ mr: '1vw', verticalAlign: 'middle' }}
                    id="partCount"
                    type='number'
                    label={"Number of Participants"}
                />
                <BlueButton idStr='addProject' style={{ verticalAlign: 'middle' }}>Add project</BlueButton>
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
                {/* downloading participants and user data */}
                <BlueButton idStr='downloadParticipants' >Download participants of selected projects</BlueButton>
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
                                    <IconButton><DeleteOutline /></IconButton>
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