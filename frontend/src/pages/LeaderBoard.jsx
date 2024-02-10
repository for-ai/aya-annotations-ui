import LeaderBoardDisplay from "../components/LeaderBoardDisplay";
import Navbar from "../components/Navbar.jsx";

const LeaderBoard = () => {
  return (
    <>
      <Navbar linkTo="/workspace" />
      <LeaderBoardDisplay />
    </>
  );
};

export default LeaderBoard;
