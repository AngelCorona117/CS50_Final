const unity = document.querySelector("#unity");
const CS50 = document.querySelector("#CS50");
const hamburguer = document.querySelector("#hamburguer-button");
const mobileOptions = document.querySelector(".mobile-options");


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

