// materials
import {
  TextField,
  IconButton,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from "@mui/material";
import {
  DeleteOutline,
  Timeline,
} from "@mui/icons-material";
import { DataGrid, GridApi, GridCellValue, GridColDef } from "@mui/x-data-grid";
import BlueButton from './../components/BlueButton';

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios'
import {authHeader} from "../helpers/auth-header";
import fileDownload from 'js-file-download';
const BASE_URL = "https://localhost:5000/projectapi";

/**
 *
 * @returns Participants Page
 */

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

      return <div><IconButton><Timeline /></IconButton><IconButton><DeleteOutline /></IconButton></div>;
    }
  }
];

const rows = [
  { id: 1, username: 'Bob', password: '123test', project: 'testProject1' },
  { id: 2, username: 'Roger', password: 'password', project: 'testProject2' },
  { id: 3, username: 'Eugene', password: 'secret', project: 'testProject3' },
  { id: 4, username: 'Alice', password: 'qwertyuiop', project: 'testProject4' },
  { id: 5, username: 'Claire', password: 'welcome1', project: 'testProject5' },
];

// replace with list of real projects, needed for project dropdowns
const projects = [
  { id: 1, projectName: 'test project 1'},
  { id: 2, projectName: 'test project 2'},
  { id: 3, projectName: 'test project 3'},
]

function Participants() {
  //set title in parent 'base'
  const { setTitle } = useOutletContext();
  useEffect(() => {
    setTitle('Participants');
  });

  // project in project add
  const [projectAdd, setProjectAdd] = useState('');
  // project in project download
  const [projectDown, setProjectDown] = useState('');

  // dropdown handler for project add
  const handleProjAddPart = (event) => {
    setProjectAdd(event.target.value);
  };

  // number of participants to add to a project
  const [participantCount, setParticipantCount] = useState(0);

  /*
   * Do POST request containing participantCount and projectAdd variable, recieve status of response.
   * When successful, download response csv file.
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
    axios.post(`${BASE_URL}/addparticipants`, data, {headers: authHeader()}).then(response =>{
      // Post request is successful, participants are registered
      // TODO: reload participant list 
      const fileName = response.headers["custom-filename"];
      fileDownload(response.data, fileName);
    }).catch(error =>{
        // Post request failed, user is not created
        console.error("Something went wrong:", error.response.data);
    });
  };

  return (
    <>
      <div style={{ textAlign: 'center', marginBottom: '1vh' }}>
        <TextField
          sx={{ mr: '1vw', verticalAlign: 'middle' }}
          id="noOfParticipants"
          label="Number of participants"
          type="number"
          value={participantCount}
          onChange={(e) => {setParticipantCount(e.target.value)}}
          InputLabelProps={{
            shrink: true,
          }}
          inputProps= {{
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
            {projects.map((inst) => <MenuItem value={inst.id}>{inst.projectName}</MenuItem>)}
          </Select>
        </FormControl>
        <BlueButton idStr='addParticipants' onClick={handleAddToProject}>Add participants</BlueButton>
      </div>
      <div className='topBorder'>
        <div style={{ paddingLeft: '2vw', display: 'inline' }} />
        <BlueButton idStr='downloadUserDataSelectedParticipants'>Download user data of selected participants</BlueButton>
      </div>
      <div style={{ justifyContent: 'center', display: 'flex' }}>
        <div style={{ height: '80vh', maxHeight: '400px', width: '50vw' }} >
          <DataGrid
            rows={rows}
            columns={columns}
            pageSize={5}
            rowsPerPageOptions={[5]}
            checkboxSelection
            disableSelectionOnClick
          />
        </div>
      </div>
    </>
  );
}

export default Participants;