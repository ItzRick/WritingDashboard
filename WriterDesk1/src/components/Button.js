import PropTypes from 'prop-types'

const Button = ({text, type}) => {
    return <button type={type}>{text}</button>
}

Button.propTypes = {
    text: PropTypes.string,
    type: PropTypes.elementType.isRequired,
}

export default Button;