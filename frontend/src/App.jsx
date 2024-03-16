import React, { Suspense } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import AuthHandler from "./components/AuthHandler.jsx";
import PrivateRoute from "./components/PrivateRoute.jsx";
import Error401 from "./pages/Error401.jsx";
import GradioAnalytics from "./pages/GradioAnalytics.jsx";
import Settings from "./pages/Settings.jsx";
import TeamPage from "./pages/TeamPage.jsx";
import UserContributionPage from "./pages/UserContributionPage/index.jsx";

const LoginCallback = React.lazy(() =>
  import("./components/LoginCallback.jsx")
);
const AnalyticsListener = React.lazy(() =>
  import("./listeners/AnalyticsListener.jsx")
);
const AddDetails = React.lazy(() => import("./pages/AddDetails.jsx"));
const Error404 = React.lazy(() => import("./pages/Error404.jsx"));
const Home = React.lazy(() => import("./pages/Home.jsx"));
const LeaderBoard = React.lazy(() => import("./pages/LeaderBoard.jsx"));
const Workspace = React.lazy(() => import("./pages/Workspace.jsx"));

const App = () => {
  return (
    <div id="app" className="App">
      <BrowserRouter>
        <AuthHandler />
        <Suspense fallback={<div>Loading...</div>}>
          <AnalyticsListener />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/callback" element={<LoginCallback />} />
            <Route path="/home" element={<Home />} />
            <Route path="/401" element={<Error401 />} />
            <Route path="/404" element={<Error404 />} />
            <Route element={<PrivateRoute />}>
              <Route path="/workspace" element={<Workspace />} />
              <Route path="/add-details" element={<AddDetails />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/leaderboard" element={<LeaderBoard />} />
              <Route path="/contributions" element={<UserContributionPage />} />
            </Route>
            <Route path="*" element={<Error404 />} />
            <Route path="/analytics" element={<GradioAnalytics />} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </div>
  );
};

export default App;
