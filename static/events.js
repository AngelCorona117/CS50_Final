
const unity = document.querySelector("#unity");
const CS50 = document.querySelector("#CS50");
const hamburguer = document.querySelector("#hamburguer-button");
const mobileOptions = document.querySelector(".mobile-options");
//NAV BAR EVENTS
unity.addEventListener("mouseover", () => {
    if (CS50.classList.contains("hidden")) {
        CS50.classList.remove("hidden");
    }
});


unity.addEventListener('mouseout', function () {
    CS50.classList.add('hidden');
});


hamburguer.addEventListener("click", () => {
    mobileOptions.classList.toggle("hidden");
});
//END NAV BAR EVENTS

if (window.location.pathname === '/user') {
    const loginButton = document.querySelector("#login-button");
    const registerButton = document.querySelector("#register-button");
    const loginForm = document.querySelector("#login-form");
    const registerForm = document.querySelector("#register-form");
    const account = document.querySelector("#account-button");
    const accountOptions = document.querySelector(".account-options");
    const logOut = document.querySelector("#log-out");


    //account options
    const accountProfileButton = document.querySelector("#balance-30-bar");
    const accountProfileBar = document.querySelector("#profile-70-bar");
    const accountSettingButton = document.querySelector("#settings-30-bar");
    const accountSettingBar = document.querySelector("#settings-70-bar");
    const fontChanger = document.querySelector("#font-change");

    const extraSmall = document.querySelector("#XS");
    const small = document.querySelector("#S");
    const medium = document.querySelector("#M");
    const large = document.querySelector("#L");
    const extraLarge = document.querySelector("#XL");
    const extraExtraLarge = document.querySelector("#XXL");
    const extraSmallSpan = document.querySelector("#extra-small");
    const smallSpan = document.querySelector("#small");
    const mediumSpan = document.querySelector("#medium");
    const largeSpan = document.querySelector("#large");
    const extraLargeSpan = document.querySelector("#extra-large");
    const extraExtraLargeSpan = document.querySelector("#extra-extra-large");


    //functions
    function change_font_size(font) {
        const elements = document.getElementsByTagName('span');
        for (let i = 0; i < elements.length; i++) {
            elements[i].style.fontSize = font;
        }
        extraSmallSpan.style.fontSize = "10px";
        smallSpan.style.fontSize = "13px";
        mediumSpan.style.fontSize = "16px";
        largeSpan.style.fontSize = "19px";
        extraLargeSpan.style.fontSize = "";
        extraExtraLargeSpan.style.fontSize = "1.6rem";
    }

    //events
    if (loginButton !== null) {
        loginButton.addEventListener("click", () => {
            if (!registerForm.classList.contains("hidden")) {
                registerForm.classList.add("hidden");
            }
            loginForm.classList.remove("hidden");
        });
    }


    if (registerButton !== null) {
        registerButton.addEventListener("click", () => {
            if (!loginForm.classList.contains("hidden")) {
                loginForm.classList.add("hidden");
            }
            registerForm.classList.remove("hidden");
        });
    }


    account.addEventListener("click", () => {
        accountOptions.classList.toggle("hidden");
    });

    logOut.addEventListener("click", () => {
        window.location.href = "/logout";
    });

    accountProfileButton.addEventListener("click", () => {
        if (!accountSettingBar.classList.contains("hidden")) {
            accountSettingBar.classList.add("hidden");
        }
        accountProfileBar.classList.toggle("hidden");
    });
    accountSettingButton.addEventListener("click", () => {
        if (!accountProfileBar.classList.contains("hidden")) {
            accountProfileBar.classList.add("hidden");
        }
        accountSettingBar.classList.toggle("hidden");
    });

    if (fontChanger !== null) {
        extraSmall.addEventListener('click', function () {
            change_font_size("0.6rem");
        });
        small.addEventListener('click', function () {
            change_font_size("0.8rem");
        });
        medium.addEventListener('click', function () {
            change_font_size("1rem");
        });
        large.addEventListener('click', function () {
            change_font_size("1.2rem");
        });
        extraLarge.addEventListener('click', function () {
            change_font_size("");
        });
        extraExtraLarge.addEventListener('click', function () {
            change_font_size("1.6rem");
        });
    }

}



