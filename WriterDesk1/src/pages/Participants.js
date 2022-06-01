// materials
import {
  TextField,
  IconButton,

} from "@mui/material";
import {
  DeleteOutline,
  Timeline,
} from "@mui/icons-material";
import { DataGrid, GridApi, GridCellValue, GridColDef} from "@mui/x-data-grid";
import BlueButton from './../components/BlueButton';

// routing
import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';



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
  {id: 1, username: 'Bob', password: '123test', project: 'testProject1'},
  {id: 2, username: 'Roger', password: 'password', project: 'testProject2'},
  {id: 3, username: 'Eugene', password: 'secret', project: 'testProject3'},
  {id: 4, username: 'Alice', password: 'qwertyuiop', project: 'testProject4'},
  {id: 5, username: 'Claire', password: 'welcome1', project: 'testProject5'},
];

function Participants() {
    //set title in parent 'base' 
    const { setTitle } = useOutletContext();
    useEffect(() => {
        setTitle('Participants');
    });
    return (
        <>
            <div style={{textAlign: 'center', marginBottom: '1vh'}}>
                <TextField
                  style={{marginRight: '1vw', marginTop: '1vw'}}
                  id="noOfParticipants"
                  label="Number of participants"
                  type="number"
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
                <TextField
                    style={{marginRight: '1vw', marginTop: '1vw'}}
                    id="projectName"
                    label={"Project name"}
                />
                <BlueButton>Add participants</BlueButton>
            </div>
            <div className='topBorder'>
                <TextField
                    style={{marginRight: '1vw', marginTop: '1vw'}}
                    id="projectName2"
                    label={"Project name"}
                />
                <BlueButton>Download participants</BlueButton>
            </div>
            <div className='topBorder'>
                <TextField
                    style={{marginRight: '1vw', marginTop: '1vw'}}
                    id="startDate"
                    label={"Start date"}
                />
                <TextField
                    style={{marginRight: '1vw', marginTop: '1vw'}}
                    id="enData"
                    label={"End date"}
                />
                <TextField
                    style={{marginRight: '1vw', marginTop: '1vw'}}
                    id="projectName3"
                    label={"Project name"}
                />
                <BlueButton>Download user data</BlueButton>
            </div>
            <div className='topBorder'>
                <Button variant='contained' style={{marginTop: '1vw', marginLeft: '1vw'}}>Download selected participants</Button>
                <div style={{paddingLeft: '2vw', display: 'inline'}} />
                <Button variant='contained' style={{marginTop: '1vw', marginLeft: '1vw'}}>Download user data of selected participants</Button>
            </div>
            <div style={{justifyContent: 'center', display: 'flex'}}>
                <div style={{height: '80vh', maxHeight: '400px', width: '50vw'}} >
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