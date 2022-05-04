import PropTypes from 'prop-types'

const SignUpInput = ({text, type, onChange}) => {
    return (
    <label>
        <p>{text}</p>
        <input type={type} onChange={onChange}/>
    </label>
    );
}

SignUpInput.propTypes = {
    text: PropTypes.string,
    type: PropTypes.elementType,
}

export default SignUpInput;