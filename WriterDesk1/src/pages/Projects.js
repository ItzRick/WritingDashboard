import {
    TextField,
    IconButton,
    Stack,
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

    // TODO remove toyData here and from tableData
    const toyData = [{
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

    //data displayed in the table
    const [tableData, setTableData] = useState(toyData)
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

    const createProject = (e) => {
        if (!(numberOfParticipants !== '' && numberOfParticipants >= 0 && numberOfParticipants <= 10000)) {
            alert('Make sure the number of participants is a valid number between 0 and 10000');
            return null;
        }
        let userId = 1; //TODO: Change to current userId

        const formData = new FormData();
        formData.append('userId', userId);
        formData.append('projectName', projectName);
        axios.post(`https://localhost:5000/projectapi/setProject`, formData).then(response => {

        });

        //TODO: Create participant accounts

    }

    const deleteProject = (e, params) => {
        // Url of the server:
        const url = 'https://127.0.0.1:5000/projectapi/deleteProject'
        // Formdata for the backend call, to which the id has been added:
        const formData = new FormData();
        formData.append('projectId', params.id);
        // Make the call to the backend:
        axios.delete(url, { data: formData }).then(response => {

        });

    }

    const deleteSelectedProjects = (e) => {
        // // Url of the server:
        // const url = 'https://127.0.0.1:5000/projectapi/projectdelete'
        // // Create a new formdata:
        // const formData = new FormData();
        // // For each of the selected instances, add this id to the formdata:
        // selectedInstances.forEach(id => alert(id));
        // // Make the backend call:
        // axios.delete(url, { data: formData })
        //   .then(() => {  });
    }


    return (
        <>
            <div style={{ height: '30%' }}>
                {/* adding projects */}
                <div style={{ textAlign: 'center', marginBottom: '1vh' }}>
                    <TextField
                        sx={{ mr: '1vw', verticalAlign: 'middle' }}
                        id="projectName"
                        label={"Project name"}
                        inputProps={{ maxLength: 264 }}
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
                    <BlueButton style={{ verticalAlign: 'middle' }} onClick={(e) => {createProject(e)}}>Add project</BlueButton>
                </div>
                <div />
                <div className="topBorder">
                    {/* downloading user data */}
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
                    <TextField
                        sx={{ margin: '1vh', verticalAlign: 'middle' }}
                        id="projectName3"
                        label={"Project name"}
                    />
                    <BlueButton style={{ margin: '1vh', verticalAlign: 'middle' }}>Download user data</BlueButton>
                </div>
                <div className="topBorder">
                    {/* downloading participants and user data */}
                    <BlueButton addStyle={{ margin: '1vh', verticalAlign: 'middle', }}>Download participants of selected projects</BlueButton>
                    <BlueButton addStyle={{ margin: '1vh', verticalAlign: 'middle', }}>Download user data of participants of selected project</BlueButton>
                </div>
            </div>
            {/* displaying projects */}
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
        </>
    );
}




export default Projects;