import { useState } from "react";

function UserRegistrationForm() {

  const [inputs, setInputs] = useState({});


  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs(values => ({...values, [name]: value}))
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    alert("You are registered !  " + { inputs } + ".")
    console.log(inputs);
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>Full Name:
      <input 
        type="text" 
        name="username" 
        value={inputs.username || ""} 
        onChange={handleChange}
      />
      </label>

      <label>Email:
      <input 
        type="text" 
        name="email" 
        value={inputs.email || ""} 
        onChange={handleChange}
      />
      </label>

      <label>Password:
      <input 
        type="text" 
        name="pass" 
        value={inputs.pass || ""} 
        onChange={handleChange}
      />
      </label>

      <label>Confirm Password:
      <input 
        type="text" 
        name="conpass" 
        value={inputs.conpass || ""} 
        onChange={handleChange}
      />
      </label>
      <label>Gender :
      <label>Male:
        <input 
          type="radio" 
          name="gender" 
          value={"male"} 
          onChange={handleChange}
        />
        </label>
        <label>Female:
        <input 
          type="radio" 
          name="gender" 
          value={"female"} 
          onChange={handleChange}
        />
        </label>
        </label>
        <label>accept terms:
        <input 
          type="checkbox" 
          name="check" 
          value={"accepted"} 
          onChange={handleChange}
        />
        </label>

        <input type="submit" 
        
        />
    </form>
      
    
  )
}
 

export default UserRegistrationForm;
