import { useContext } from "react";
import { User } from "../../pages/website/context/UserContext";

function Home() {
  const { auth } = useContext(User);

  return (
    <div>
      <h2>Welcome To Secure GBooking</h2>
      {auth?.userDetails?.name && (
        <p>Hello, <strong>{auth.userDetails.name}</strong> 👋</p>
      )}
    </div>
  );
}

export default Home;
