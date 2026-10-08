/* =====================================================
   EVENTEASE
   Main JavaScript
===================================================== */


/* =====================================================
   MOBILE MENU
===================================================== */

function toggleMenu() {

    const nav = document.querySelector(".nav-links");

    nav.classList.toggle("show");

}


/* =====================================================
   EVENT FILTER
===================================================== */

function filterEvents(category, button) {

    const events =
        document.querySelectorAll(".event-item");

    const buttons =
        document.querySelectorAll(".filter-btn");


    buttons.forEach(function (btn) {

        btn.classList.remove("active-filter");

    });


    button.classList.add("active-filter");


    events.forEach(function (event) {

        const eventCategory =
            event.getAttribute("data-category");


        if (category === "all") {

            event.style.display = "";

        }

        else if (eventCategory === category) {

            event.style.display = "";

        }

        else {

            event.style.display = "none";

        }

    });

}


/* =====================================================
   SELECT EVENT
===================================================== */

function selectEvent(eventName) {

    const eventSelect =
        document.getElementById("event");


    if (eventSelect) {

        eventSelect.value = eventName;

    }


    const registerSection =
        document.getElementById("register");


    if (registerSection) {

        registerSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    }

}


/* =====================================================
   FORM VALIDATION + DJANGO SUBMISSION
===================================================== */

const registrationForm =
    document.getElementById("registrationForm");


if (registrationForm) {

    registrationForm.addEventListener(
        "submit",
        function (e) {

            /*
                IMPORTANT:

                Do NOT call e.preventDefault()
                here.

                If the form is valid, it must
                be submitted normally to Django.
            */


            const name =
                document.getElementById("name")
                    .value.trim();


            const email =
                document.getElementById("email")
                    .value.trim();


            const phone =
                document.getElementById("phone")
                    .value.trim();


            const department =
                document.getElementById("department")
                    .value;


            const eventName =
                document.getElementById("event")
                    .value;


            const terms =
                document.getElementById("terms")
                    .checked;


            /* -------------------------------
               ERROR ELEMENTS
            -------------------------------- */

            const nameError =
                document.getElementById("nameError");


            const emailError =
                document.getElementById("emailError");


            const phoneError =
                document.getElementById("phoneError");


            const departmentError =
                document.getElementById("departmentError");


            const eventError =
                document.getElementById("eventError");


            const termsError =
                document.getElementById("termsError");


            /* -------------------------------
               CLEAR PREVIOUS ERRORS
            -------------------------------- */

            nameError.textContent = "";
            emailError.textContent = "";
            phoneError.textContent = "";
            departmentError.textContent = "";
            eventError.textContent = "";
            termsError.textContent = "";


            let valid = true;


            /* =================================================
               NAME
            ================================================= */

            const namePattern =
                /^[A-Za-z ]{3,}$/;


            if (name === "") {

                nameError.textContent =
                    "Please enter your name.";

                valid = false;

            }

            else if (!namePattern.test(name)) {

                nameError.textContent =
                    "Please enter a valid name.";

                valid = false;

            }


            /* =================================================
               EMAIL
            ================================================= */

            const emailPattern =
                /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


            if (email === "") {

                emailError.textContent =
                    "Please enter your email.";

                valid = false;

            }

            else if (!emailPattern.test(email)) {

                emailError.textContent =
                    "Please enter a valid email.";

                valid = false;

            }


            /* =================================================
               PHONE
            ================================================= */

            const phonePattern =
                /^\d{10}$/;


            if (phone === "") {

                phoneError.textContent =
                    "Please enter your phone number.";

                valid = false;

            }

            else if (!phonePattern.test(phone)) {

                phoneError.textContent =
                    "Enter a valid 10-digit number.";

                valid = false;

            }


            /* =================================================
               DEPARTMENT
            ================================================= */

            if (department === "") {

                departmentError.textContent =
                    "Please select your department.";

                valid = false;

            }


            /* =================================================
               EVENT
            ================================================= */

            if (eventName === "") {

                eventError.textContent =
                    "Please choose an event.";

                valid = false;

            }


            /* =================================================
               TERMS
            ================================================= */

            if (!terms) {

                termsError.textContent =
                    "Please accept the terms.";

                valid = false;

            }


            /* =================================================
               STOP ONLY IF INVALID
            ================================================= */

            if (!valid) {

                e.preventDefault();

            }

            /*
                If valid == true:

                We DON'T call preventDefault().

                Therefore the browser submits:

                POST → Django home view
                → RegistrationForm
                → form.save()
                → SQLite
                → redirect('home')
            */

        }
    );

}


/* =====================================================
   ACTIVE NAVIGATION
===================================================== */

const sections =
    document.querySelectorAll("section[id]");


const navLinks =
    document.querySelectorAll(".nav-links a");


window.addEventListener(
    "scroll",
    function () {

        let current = "";


        sections.forEach(function (section) {

            const sectionTop =
                section.offsetTop - 100;


            if (window.scrollY >= sectionTop) {

                current =
                    section.getAttribute("id");

            }

        });


        navLinks.forEach(function (link) {

            link.classList.remove("active");


            if (
                link.getAttribute("href") ===
                "#" + current
            ) {

                link.classList.add("active");

            }

        });

    }
);


/* =====================================================
   CLOSE MOBILE MENU AFTER CLICK
===================================================== */

navLinks.forEach(function (link) {

    link.addEventListener(
        "click",
        function () {

            const nav =
                document.querySelector(".nav-links");

            nav.classList.remove("show");

        }
    );

});

