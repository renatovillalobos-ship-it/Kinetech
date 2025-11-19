/*
        Designed by: SELECTO
        Original image: https://dribbble.com/shots/5311359-Diprella-Login
*/

let switchCtn = document.querySelector("#switch-cnt");
let switchC1 = document.querySelector("#switch-c1");
let switchC2 = document.querySelector("#switch-c2");
let switchCircle = document.querySelectorAll(".switch__circle");
let switchBtn = document.querySelectorAll(".switch-btn");
let aContainer = document.querySelector("#a-container");
let bContainer = document.querySelector("#b-container");
let allButtons = document.querySelectorAll(".submit");

let changeForm = (e) => {
    switchCtn.classList.add("is-gx");
    setTimeout(function(){
        switchCtn.classList.remove("is-gx");
    }, 1500)

    switchCtn.classList.toggle("is-txr");
    switchCircle[0].classList.toggle("is-txr");
    switchCircle[1].classList.toggle("is-txr");

    switchC1.classList.toggle("is-hidden");
    switchC2.classList.toggle("is-hidden");
    aContainer.classList.toggle("is-txl");
    bContainer.classList.toggle("is-txl");
    bContainer.classList.toggle("is-z200");
}

let mainF = (e) => {
    for (var i = 0; i < switchBtn.length; i++)
        switchBtn[i].addEventListener("click", changeForm)
}

window.addEventListener("load", mainF);

// === CAMBIO ENTRE FORMULARIOS DOCENTE Y ESTUDIANTE ===
const docenteForm = document.getElementById("docente-form");
const estudianteForm = document.getElementById("estudiante-form");

// Obtener TODOS los botones por clase
const docenteBtns = document.querySelectorAll(".docente-btn");
const estudianteBtns = document.querySelectorAll(".estudiante-btn");

// Agregar evento a TODOS los botones de docente
docenteBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        if (docenteForm && estudianteForm) {
            docenteForm.style.display = "flex";
            estudianteForm.style.display = "none";
        }
    });
});

// Agregar evento a TODOS los botones de estudiante
estudianteBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        if (docenteForm && estudianteForm) {
            estudianteForm.style.display = "flex";
            docenteForm.style.display = "none";
        }
    });
});