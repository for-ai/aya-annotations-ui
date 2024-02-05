import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { useSetRecoilState } from "recoil";

import { isAuthenticated } from "../helpers/auth.jsx";
import { isAuthenticatedState } from "../recoil/atoms/isAuthenticatedState.jsx";

const AuthHandler = () => {
  const setIsAuthenticatedState = useSetRecoilState(isAuthenticatedState);
  const location = useLocation();

  useEffect(() => {
    (async () => {
      const auth = await isAuthenticated();
      setIsAuthenticatedState(auth);
    })();
  }, [location, setIsAuthenticatedState]);

  return null;
};

export default AuthHandler;
