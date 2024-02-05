import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { handleLoginCallback } from "../helpers/auth.jsx";
import { trackUserNewGA, trackUserReturnGA } from "../helpers/ga.jsx";

const LoginCallback = () => {
  const navigateTo = useNavigate();

  // LoginCallback the user and redirect
  useEffect(() => {
    // Get the URL parameters which will include the auth token
    let params = new URLSearchParams(window.location.search);

    handleLoginCallback(params)
      .then((isCompleteProfile) => {
        if (isCompleteProfile) {
          trackUserReturnGA();
          navigateTo("/workspace");
        } else {
          trackUserNewGA();
          navigateTo("/add-details");
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }, [navigateTo]);

  return <></>;
};

export default LoginCallback;
