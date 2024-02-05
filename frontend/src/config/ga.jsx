import ReactGA from "react-ga4";

const trackingID = process.env.GOOGLE_ANALYTICS_ID;

ReactGA.initialize([
  {
    trackingId: trackingID,
  },
]);

const _ga = ReactGA;

export default _ga;
