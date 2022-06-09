// materials
import {
    Button,
    TextField
} from "@mui/material";

/**
 * 
 * @returns Single File Upload Object
 */
 const UploadSingleFile = () => {
    return(
        <div style={{marginBottom: '1vw'}}>
            <div className='vertCenter'>
                <div className='upload'>
                    <Button variant='contained' sx={{mr: '8px', bgcolor: 'button.main', color: 'button.text'}}>Choose a file</Button>
                    or drag it here.
                </div>
                <TextField label='dd/mm/yy' variant='outlined' style={{marginRight: '1vw'}}/>
                <TextField label='course' variant='outlined'/>
            </div>
        </div>
)};

export default UploadSingleFile;