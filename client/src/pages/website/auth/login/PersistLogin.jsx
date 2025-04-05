import { useContext, useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import { User } from "../../context/UserContext";
import Cookies from "universal-cookie";
import Loading from "../../../../components/Loading";
import { apiPost } from '../../../../api/apiMethods';

export default function PersistLogin() {
  const { auth, setAuth } = useContext(User);
  const [loading, setLoading] = useState(true);
  const cookie = new Cookies();

  const accessToken = auth.access_token;
  const refreshToken = cookie.get("refresh_token");


  useEffect(() => {
    async function refresh() {
      console.log("Attempting to refresh token...");
      try {
        const res = await apiPost('auth/refresh', {
          refresh_token: refreshToken
        });

        console.log("Refresh successful:", res);

        localStorage.setItem("access_token", res.access_token);
        cookie.set("access_token", res.access_token);

        if (res.refresh_token) {
          localStorage.setItem("refresh_token", res.refresh_token);
          cookie.set("refresh_token", res.refresh_token);
        }

        if (res.user_details) {
          localStorage.setItem("user_details", JSON.stringify(res.user_details));
        }

        setAuth({
          access_token: res.access_token,
          userDetails: res.user_details,
        });
      } catch (err) {
        console.error("Refresh token failed:", err);
      } finally {
        setLoading(false);
      }
    }

    if (!accessToken && refreshToken) {
      refresh();
    } else {
      setLoading(false);
    }
  }, []);

  if (loading) {
    return <Loading />;
  }

  return <Outlet />;
}
