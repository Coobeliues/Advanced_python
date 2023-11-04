import './App.css';
import { Outlet } from "react-router-dom";
import Login from "./components/Login"
import Profile from "./components/Profile";
import Services from "./components/Services";
function App() {
  return (
    <>
    <Login/>

      <Services/>
    {/* <Outlet/> */}
    </>
  );
}

export default App;
