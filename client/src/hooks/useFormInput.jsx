import { useState, useEffect } from 'react';

const useFormInput = (initialValue, validationRegex, validationMessages) => {
  const [value, setValue] = useState(initialValue);
  const [instruction, setInstruction] = useState();
  const [valid, setValid] = useState(false);
  const [focus, setFocus] = useState(false);

  const handleChange = (e) => {
    const newValue = e.target.value;
    setValue(newValue);
  };

  const handleFocus = () => {
    setFocus(true);
  };

  const handleBlur = () => {
    setFocus(false);
  };

  useEffect(() => {
    setValid(validationRegex.test(value));
    setInstruction(validationMessages);
  }, [value, validationRegex,validationMessages]);

  return {
    value,
    setValue,
    valid,
    focus,
    instruction,
    handleChange,
    handleFocus,
    handleBlur, 
  };
};

export default useFormInput;
