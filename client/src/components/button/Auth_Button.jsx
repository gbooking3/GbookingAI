/* eslint-disable react/prop-types */
import './Auth_Button.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

const Auth_Button = ({ validation, name, loading }) => {
  return (
    <div className="auth">
      <button
        type="submit"
        className="auth"
        disabled={!validation || loading}
      >
        {loading ? (
          <FontAwesomeIcon icon={faSpinner} spin />
        ) : (
          name
        )}
      </button>
    </div>
  );
};

export default Auth_Button;
