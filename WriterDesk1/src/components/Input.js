import PropTypes from 'prop-types'

const Input = ({text, type, onChange}) => {
    return (
    <label>
        <p>{text}</p>
        <input type={type} onChange={onChange}/>
    </label>
    );
}

Input.propTypes = {
    text: PropTypes.string,
    type: PropTypes.elementType,
}

export default Input;