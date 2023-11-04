import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { createBrowserRouter, Routes, Route, RouterProvider } from "react-router-dom";
import Login from "./components/Login"
import Profile from "./components/Profile"
import Services from "./components/Services";
const root = ReactDOM.createRoot(document.getElementById('root'));
const router = createBrowserRouter([
      {
        path: "/auth/login",
        element: <Login/>,
      },
      {
        path: "/profile",
        element: <Profile/>,
      },
      {
        path: "/services",
        element: <Services/>,
      },
])

root.render(
    <RouterProvider router = {router} />
);