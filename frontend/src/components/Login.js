import React, { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';
import { Link } from "react-router-dom";

const Login = () => {
    const navigate = useNavigate();
    const f = () => {
        navigate('/services');
    }
    return (
        <>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"></link>
        <nav class="navbar navbar-expand-lg navbar-custom">
            <div class="container">
                <a class="navbar-brand mr-auto" href="#">Egov | 1414</a>
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="#" id="register-button">Register</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="languageDropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Language</a>
                        <div class="dropdown-menu" aria-labelledby="languageDropdown">
                            <a class="dropdown-item" href="javascript:void(0);" onclick="changeLanguage('KZ')">KZ</a>
                            <a class="dropdown-item" href="javascript:void(0);" onclick="changeLanguage('RU')">RU</a>
                            <a class="dropdown-item" href="javascript:void(0);" onclick="changeLanguage('EN')">EN</a>
                        </div>
                    </li>
                </ul>
            </div>
        </nav>

        <div class="content">
            <div class="container">
                <div class="row justify-content-center align-items-center">
                    <div class="col-md-6">
                        <div class="additional-text">
                            <p>
                                <span class="green-text" id="additional-text"></span>
                                <br />
                                <span id="additional-text-content"></span>
                            </p>
                        </div>
                        <div class="card">
                            <div class="card-header">
                                <h3 class="text-center" id="card-header"></h3>
                            </div>
                            <div class="card-body">
                                <form action="/auth/login/" method="POST">
                                    <div class="mb-3 text-center">
                                        <label for="username" class="form-label" id="username-label"></label>
                                        <input type="text" placeholder="Username" name="username" class="form-control" id="username"/>
                                    </div>
                                    <div class="mb-3 text-center">
                                        <label for="password" class="form-label" id="password-label"></label>
                                        <input type="password" placeholder="Password" name="password" class="form-control" id="password"/>
                                    </div>
                                    <div class="mb-3">
                                        <button type="button" class="btn btn-primary" id="sign-in-button"  onClick={() => f()}>Sign In</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">© <span id="footer-text"></span></div>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        <script src="script.js"></script>
        </>
    )
}

export default Login;