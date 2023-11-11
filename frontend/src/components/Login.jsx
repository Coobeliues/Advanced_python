import React, {useContext, useState} from 'react';
import {UserContext} from "../context/UserContext";
import './Login.css';
// import './script.js'
import "https://code.jquery.com/jquery-3.5.1.slim.min.js"
import "https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"
import "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"

import {Link, useNavigate} from "react-router-dom";

const languageData = {
    KZ: {
        "register-button": "Тіркелу",
        "additional-text": "Құрметті пайдаланушылар!",
        "additional-text-content":
            "Сіздің бейініңіздің қауіпсіздігін арттыру және қорғау мақсатында Сізге авторизациялау көп факторлы авторизация (логин (ЖСН/БСН) және пароль енгізілгеннен кейін ЭЦҚ міндетті түрде қол қою) қолданылатынын хабарлаймыз.Осы тәсіл Қазақстан Республикасы Үкіметінің 2016 жылғы 20 желтоқсандағы №832 қаулысымен бекітілген ақпараттық-коммуникациялық технологиялар және ақпараттық қауіпсіздікті қамтамасыз ету саласындағы бірыңғай талаптарға сәйкес енгізіледі.",
        "card-header": "Порталға кіру",
        "username-label": "Логин",
        "password-label": "Пароль",
        "sign-in-button": "Жүйеге кіру",
        "footer-text": "Қазақстан Республикасының Электрондық үкіметі",
    },
    RU: {
        "register-button": "Зарегистрироваться",
        "additional-text": "Уважаемые пользователи!",
        "additional-text-content":
            "В целях повышения безопасности и защиты Вашего профиля, уведомляем Вас, что в процессе авторизации применяется многофакторная авторизация (обязательное смс подтверждение после ввода Логина (ИИН/БИН) и пароля).Данный подход внедряется в соответствии с Едиными требованиями в области информационно-коммуникационных технологий и обеспечения информационной безопасности, утвержденным Постановлением Правительства Республики Казахстан от 20 декабря 2016 года №832.",
        "card-header": "Вход на портал",
        "username-label": "Логин",
        "password-label": "Пароль",
        "sign-in-button": "Войти в систему",
        "footer-text": "Электронное правительство Республики Казахстан",
    },
    EN: {
        "register-button": "Sign up",
        "additional-text": "Dear users!",
        "additional-text-content":
            "For the purpose of enhancing security and protecting your profiles, we inform you that multi-factor authorization (mandatory confirmation by entering SMS code after entering a login (IIN/BIN) and password) is used during the authorization process. The approach is being implemented pursuant to the Single Requirements in the field of information and communication technologies and information security approved by the Decree of the Government of the Republic of Kazakhstan as of December 20, 2016 No. 832.",
        "card-header": "Login to the portal",
        "username-label": "Username",
        "password-label": "Password",
        "sign-in-button": "Sign In",
        "footer-text":
            "Electronic Government of the Republic of Kazakhstan",
    },
    };

const Login = () => {
    const navigate = useNavigate();
    const [, setToken] = useContext(UserContext);

    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });
    const [errorMessage, setErrorMessage] = useState('');

    const changeLanguage = (language) => {
        const elements = Object.keys(languageData[language]);
        elements.forEach((element) => {
            const elementId = document.getElementById(element);
            if (elementId) {
                elementId.textContent = languageData[language][element];
            }
        });

        const languageDropdown = document.querySelector('#languageDropdown');
        if (languageDropdown) {
            languageDropdown.textContent = language;
        }
    };

    // Initial language setup
    changeLanguage('EN');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Send the login data to your backend for authentication
        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
            const data = await response.json();
            if (response.ok) {
                console.log('Login successful');
                setToken(data.access_token);
                navigate("/");
            } else {
                setErrorMessage(data.detail);
            }
        } catch (error) {
            console.error('Login error:', error);
            setErrorMessage('An error occurred during login.');
        }
    };

    return (
        <>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"></link>
            <nav className="navbar navbar-expand-lg navbar-custom">
                <div className="container">
                    <a className="navbar-brand mr-auto" href="#">Egov | 1414</a>
                    <ul className="navbar-nav ml-auto">
                        <li className="nav-item">
                            <Link className="nav-link" href="#" id="register-button" to='/auth/register'>Register</Link>
                        </li>
                        <li className="nav-item dropdown">
                            <a className="nav-link dropdown-toggle" href="#" id="languageDropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Language</a>
                            <div className="dropdown-menu" aria-labelledby="languageDropdown">
                                <button className="dropdown-item" onClick={() => changeLanguage('KZ')}>KZ</button>
                                <button className="dropdown-item" onClick={() => changeLanguage('RU')}>RU</button>
                                <button className="dropdown-item" onClick={() => changeLanguage('EN')}>EN</button>
                            </div>
                        </li>
                    </ul>
                </div>
            </nav>

            <div className="content">
                <div className="container">
                    <div className="row justify-content-center align-items-center">
                        <div className="col-md-6">
                            <div className="additional-text">
                                <p>
                                    <span className="green-text" id="additional-text"></span>
                                    <br />
                                    <span id="additional-text-content"></span>
                                </p>
                            </div>
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="text-center" id="card-header"></h3>
                                </div>
                                <div className="card-body">
                                    <form onSubmit={handleSubmit}>
                                        <div className="mb-3 text-center">
                                            <label htmlFor="username" className="form-label" id="username-label"></label>
                                            <input  className="form-control" type="text" name="username" placeholder="Username" value={formData.username} onChange={handleInputChange} required/>
                                        </div>
                                        <div className="mb-3 text-center">
                                            <label htmlFor="password" className="form-label" id="password-label"></label>
                                            <input className="form-control" type="password" name="password" placeholder="Password" value={formData.password} onChange={handleInputChange} required
                                                        />
                                        </div>
                                        <div className="mb-3">
                                            <button type="submit" className="btn btn-primary" id="sign-in-button">Sign In</button>
                                        </div>
                                    </form>
                                    {errorMessage && <p className="error-message">{errorMessage}</p>}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="footer">© <span id="footer-text"></span></div>
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

        </>
    );
};

export default Login;
