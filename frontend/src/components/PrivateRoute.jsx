import React, { useEffect, useState } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useRecoilValue, useSetRecoilState } from "recoil";

import { isAuthenticated } from "../helpers/auth.jsx";
import { isAuthenticatedState } from "../recoil/atoms/isAuthenticatedState.jsx";

const PrivateRoute = ({ element, ...rest }) => {
  const [isAuthenticating, setIsAuthenticating] = useState(true);
  const isAuthenticatedRecoil = useRecoilValue(isAuthenticatedState);
  const setIsAuthenticatedState = useSetRecoilState(isAuthenticatedState);
  const location = useLocation();

  useEffect(() => {
    const checkAuthentication = async () => {
      const auth = await isAuthenticated();
      setIsAuthenticatedState(auth);
      setIsAuthenticating(false);
    };
    checkAuthentication();
  }, [location, setIsAuthenticatedState]);

  if (isAuthenticating) {
    return null; // Or a loading spinner
  }

  if (!isAuthenticatedRecoil) {
    return <Navigate to="/401" />;
  }

  return <Outlet {...rest} />;
};

export default PrivateRoute;
