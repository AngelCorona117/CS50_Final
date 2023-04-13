
const unity = document.querySelector("#unity");
const CS50 = document.querySelector("#CS50");
const hamburguer = document.querySelector("#hamburguer-button");
const mobileOptions = document.querySelector(".mobile-options");
const loginButton = document.querySelector("#login-button");
const registerButton = document.querySelector("#register-button");
const loginForm = document.querySelector("#login-form");
const registerForm = document.querySelector("#register-form");
console.log(loginForm);
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

loginButton.addEventListener("click", () => {
    if (!registerForm.classList.contains("hidden")) {
        registerForm.classList.add("hidden");
    }
    loginForm.classList.remove("hidden");
});
registerButton.addEventListener("click", () => {
    if (!loginForm.classList.contains("hidden")) {
        loginForm.classList.add("hidden");
    }
    registerForm.classList.remove("hidden");
});

