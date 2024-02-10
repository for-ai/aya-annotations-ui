import { useEffect } from "react";
import { useLocation } from "react-router-dom";

import ReactGA from "../config/ga.jsx";

const AnalyticsListener = () => {
  const location = useLocation();

  useEffect(() => {
    ReactGA.send({
      hitType: "pageview",
      page: location.pathname + location.search,
      title: location.pathname + location.search,
    });
  }, [location]);

  return null;
};

export default AnalyticsListener;
