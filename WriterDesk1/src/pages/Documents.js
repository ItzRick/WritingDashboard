import { useOutletContext } from 'react-router-dom';
import { useEffect } from 'react';
import {Button} from "@mui/material";
import {DataGrid} from "@mui/x-data-grid";
import {GridColDef} from "@mui/x-data-grid";
import {GridValueGetterParams} from "@mui/x-data-grid";
import IconButton from "@mui/material/IconButton";
import GradingIcon from '@mui/icons-material/Grading';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import {GridApi} from "@mui/x-data-grid";
import {GridCellValue} from "@mui/x-data-grid";


/**
 * 
 * @returns Documents Page
 */

const columns: GridColDef[] = [
  {
    field: 'filename',
    headerName: 'Filename',
    editable: false,
  },
  {
    field: 'type',
    headerName: 'Type',
    editable: false,
  },
  {
    field: 'course',
    headerName: 'Course',
    editable: false,
  },
  {
    field: 'h1',
    headerName: 'h1',
    type: "number",
    editable: false,
  },
  {
    field: 'h2',
    headerName: 'h2',
    type: "number",
    editable: false,
  },
  {
    field: 'h3',
    headerName: 'h3',
    type: "number",
    editable: false,
  },
  {
    field: 'h4',
    headerName: 'h4',
    type: "number",
    editable: false,
  },
  {
    field: 'date',
    headerName: 'Date ',
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

      return <div><IconButton><GradingIcon /></IconButton><IconButton><DeleteOutlineIcon /></IconButton></div>;
    }
  }
];

const rows = [
  {id: 1, filename: 'Test Name', type: 'PDF', course: 'Test Course', h1: 6, h2: 8, h3: 4, h4: 6, date: '11/2/2020'},
  {id: 2, filename: 'Test Name2', type: 'docx', course: 'Test Course2', h1: 3, h2: 1, h3: 4, h4: 8, date: '11/2/2020'},
  {id: 3, filename: 'Test Name3', type: 'PDF', course: 'Test Course3', h1: 5, h2: 7, h3: 2, h4: 10, date: '11/2/2020'},
  {id: 4, filename: 'Test Name4', type: 'txt', course: 'Test Course4', h1: 7, h2: 8, h3: 1, h4: 4, date: '11/2/2020'},
  {id: 5, filename: 'Test Name5', type: 'PDF', course: 'Test Course5', h1: 2, h2: 8, h3: 7, h4: 6, date: '11/2/2020'}
];

function Documents() {
  //set title in parent 'base' 
  const { setTitle } = useOutletContext();
  useEffect(() => {
    setTitle('Documents');
  });
  
  return (
    <>
      <div style={{height: '80vh', maxHeight: '400px'}} >
        <DataGrid
          rows={rows}
          columns={columns}
          pageSize={5}
          rowsPerPageOptions={[5]}
          checkboxSelection
          disableSelectionOnClick
        />
      </div>
    </>
  );
}

export default Documents;