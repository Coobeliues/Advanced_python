import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { UserProvider } from "./context/UserContext";
import Login from "./components/Login";
import Register from "./components/Register";
import Services from "./components/Services";
import Profile from "./components/Profile";
const root = ReactDOM.createRoot(document.getElementById('root'));
const router = createBrowserRouter([
    {
        path: "/",
        element: <App/>,
        children: [
        ]
    },
    {
        path: "auth/login",
        element: <Login/>,
    },
    {
        path: "auth/register",
        element: <Register/>,
    },
    {
        path: "profile",
        element: <Profile/>,
    },
    {
        path: "services",
        element: <Services/>,
    },

])
root.render(
    <UserProvider>
        <RouterProvider router = {router} />
    </UserProvider>,

);