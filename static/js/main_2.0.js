// __author__ = "Dan-Gabriel Pintoiu"
// __copyright__ = "Copyright (C) 2020 Dan-Gabriel Pintoiu"
// __license__ = "Public Domain"


// hidden elements that become visible once an action is done on the page
// eg: when an user wants to add a new employee, the form divs become visible and the original div changes its size
document.getElementById("userForm").style.display = "none";
if (document.getElementById("safeCheck")!== null) document.getElementById("safeCheck").style.display = "none";
if (document.getElementById("empCheck")!== null) document.getElementById("empCheck").style.display = "none";
if (document.getElementById("max")!== null) document.getElementById("max").style.visibility = "hidden";
if (document.getElementById("empName")!== null) document.getElementById("empName").style.display = "none";
document.getElementById("validationDate").valueAsDate = new Date();

// make the userform visible upon calling the function and resize several elements in the page
function visible() {
    document.getElementById("alwaysOnMenu").classList.remove("col-12");
    document.getElementById("alwaysOnMenu").classList.add("col-6");
    document.getElementById("userForm").classList.remove("col-0");
    document.getElementById("userForm").classList.add("col-6");
    document.getElementById("userForm").style.display = "block";
}

// cancel the above changes and delete any potential values sent to the dateObj object
function notVisible() {
    document.getElementById("alwaysOnMenu").classList.remove("col-6");
    document.getElementById("alwaysOnMenu").classList.add("col-12");
    document.getElementById("userForm").classList.remove("col-6");
    document.getElementById("userForm").classList.add("col-0");
    document.getElementById("userForm").style.display = "none";
    document.getElementById("validationName").value = "";
    document.getElementById("validationDepartment").value = "";
}

// make the limit form for the employee threshold visible for the user and make sure the span element is hidden
// if the form is already visible, hide it
function setMax() {
    if (document.getElementById("max").style.visibility == "visible") {
        document.getElementById("max").style.visibility = "hidden";
    } else {
        document.getElementById("max").style.visibility = "visible";
    }
    document.getElementById("safeCheck").style.display = "none";
}

// verify the user added value and send a jquery ajax post request
// if the value is a positive number, else return a span html element
function setMaxDone() {
    document.getElementById("max").style.visibility = "hidden";
    var value = Number(document.getElementById("max-text").value)
    
    if (Number.isInteger(value) && value > 0) {
        document.getElementById("safeCheck").style.display = "none";
        var url = "/employeeCount";
        var data = {data: value};
        $.ajaxSetup({async: false});
        $.post(url, data);
        document.location.reload(true);
    } else {
        document.getElementById("safeCheck").style.display = "block";
    }
}

function setEmp() {
    if (document.getElementById("empName").style.display == "block") {
        document.getElementById("empName").style.display = "none";
        document.getElementById("empCheck").style.display = "none";
    } else {
        document.getElementById("empName").style.display = "block";
    }
}

// verify the user added value and send a SQLAlchemy query request
// if the field is empty, return a span html element
function setEmpDone() {
    var value = document.getElementById("max-text").value
    if (value !== "") {
        window.location = "individualRemove/" + value;
    } else {
        document.getElementById("empCheck").style.display = "block";
    }
}

// bootstrap validation script
(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();
