import {
    Button,

} from "@mui/material";

const TestingComponent = ({thisIndex, setInstanceList}) => {
    const removeInstance = () => {
        setInstanceList((instanceList) => instanceList.filter(item => item.props.thisIndex !== thisIndex));
    }

    return (
        <div className='TestingComponent vertCenter'>
            <Button variant='contained' sx={{bgcolor: 'red', color: 'button.text'}} value={thisIndex}  onClick={removeInstance}>Remove {thisIndex}</Button>
        </div>
    );
}

export default TestingComponent