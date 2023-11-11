function changeLanguage(language) {
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

    const elements = Object.keys(languageData[language]);
    elements.forEach((element) => {
        const elementId = document.getElementById(element);
        if (elementId) {
            elementId.textContent = languageData[language][element];
        }
    });

    const languageDropdown = document.querySelector("#languageDropdown");
    if (languageDropdown) {
        if (language === "KZ") {
            languageDropdown.textContent = "KZ";
        } else if (language === "RU") {
            languageDropdown.textContent = "RU";
        } else if (language === "EN") {
            languageDropdown.textContent = "EN";
        }
    }
}

changeLanguage("EN");
