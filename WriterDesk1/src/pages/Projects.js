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
            <div style={{ height: '30%' }}>
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
                    <BlueButton style={{ verticalAlign: 'middle' }}>Add project</BlueButton>
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
                            <IconButton><DeleteOutline /></IconButton>
                        </GridToolbarContainer>
                    )
                }}
            />
        </>
    );
}




export default Projects;