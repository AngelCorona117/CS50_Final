
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
    const accountProfileBar= document.querySelector("#profile-70-bar");

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
        accountProfileBar.classList.toggle("hidden");
    });
}



