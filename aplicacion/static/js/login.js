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




//let getButtons = (e) => e.preventDefault()




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
    //for (var i = 0; i < allButtons.length; i++)
      //  allButtons[i].addEventListener("click", getButtons );
    for (var i = 0; i < switchBtn.length; i++)
        switchBtn[i].addEventListener("click", changeForm)
}





window.addEventListener("load", mainF);


    // 1. Elementos del Switch de Rol (Asegúrate de que estos IDs existan en login.html)
    const estudianteRoleBtn = document.getElementById("estudiante-role-btn");
    const docenteRoleBtn = document.getElementById("docente-role-btn");  


    const estudianteForm = document.getElementById("estudiante-form");
    const docenteForm = document.getElementById("docente-form");    




    // 2. Lógica para alternar la visibilidad de los formularios
    if (docenteRoleBtn && estudianteRoleBtn && docenteForm && estudianteForm) {
    
        // Al hacer clic en el botón DOCENTE:
        docenteRoleBtn.addEventListener("click", () => {
            // Muestra el formulario de Docente
            docenteForm.classList.remove("is-hidden");
            // Oculta el formulario de Estudiante
            estudianteForm.classList.add("is-hidden");
        
            // Opcional: Manejo de estilos para resaltar el botón activo
            docenteRoleBtn.classList.add("is-active");
            estudianteRoleBtn.classList.remove("is-active");
        });


        // Al hacer clic en el botón ESTUDIANTE:
        estudianteRoleBtn.addEventListener("click", () => {
            // Muestra el formulario de Estudiante
            estudianteForm.classList.remove("is-hidden");
            // Oculta el formulario de Docente
            docenteForm.classList.add("is-hidden");
        
            // Opcional: Manejo de estilos para resaltar el botón activo
            docenteRoleBtn.classList.remove("is-active");
            estudianteRoleBtn.classList.add("is-active");
        });
    }