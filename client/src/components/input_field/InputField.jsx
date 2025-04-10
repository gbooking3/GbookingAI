/* eslint-disable react/prop-types */
import { MDBInput } from "mdb-react-ui-kit";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCheck,
  faTimes,
  faInfoCircle,
} from "@fortawesome/free-solid-svg-icons";

const InputField = ({
  type,
  label,
  value,
  onChange,
  valid,
  focus,
  blur,
  placeholder,
  instruction,
  allowInstructionMessages = true,
}) => {
  return (
    <div className="mb-3">
      <div className="position-relative">
        <MDBInput
          wrapperClass="mb-0"
          type={type}
          id={label}
          label={label}
          value={value}
          onChange={onChange}
          valid={valid ? "true" : undefined}
          aria-describedby={`${label}note`}
          onFocus={focus}
          onBlur={blur}
          placeholder={placeholder}
        />
        {allowInstructionMessages && (
          <div
            className="position-absolute"
            style={{ top: "50%", right: "10px", transform: "translateY(-50%)" }}
          >
            <FontAwesomeIcon
              icon={faCheck}
              className={valid ? "text-success" : "d-none"}
            />
            <FontAwesomeIcon
              icon={faTimes}
              className={valid || !value ? "d-none" : "text-danger ms-2"}
            />
          </div>
        )}
      </div>

      {allowInstructionMessages && focus && !valid && value && (
        <div
          id={`${label}note`}
          className="alert alert-danger d-flex align-items-center mt-2 py-2 px-2"
          style={{ fontSize: "0.875rem", width: "95%" }}
        >
          <FontAwesomeIcon icon={faInfoCircle} className="me-2" />
          <span className="text-start">
            {instruction}
          </span>

        </div>
      )}
    </div>
  );
};

export default InputField;
