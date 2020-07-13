// __author__ = "Dan-Gabriel Pintoiu"
// __copyright__ = "Copyright (C) 2020 Dan-Gabriel Pintoiu"
// __license__ = "Public Domain"


// hidden elements that become visible once an action is done on the page
// eg: when an user wants to add a new employee, the form divs become visible and the original div changes its size
document.getElementById("userForm").style.display = "none";
document.getElementsByClassName("date")[0].style.display = "none";
if (document.getElementById("max")!== null) document.getElementById("max").style.visibility = "hidden";
if (document.getElementById("safeCheck")!== null) document.getElementById("safeCheck").style.display = "none";
document.getElementById("validationDate2").style.display = "none";

// create an object to store the month and day from the user
var date = ""
var dateObj = {
    day: "",
    month: ""
}

// make the userform visible upon calling the function and resize several elements in the page
function visible() {
    document.getElementById("alwaysOnMenu").classList.remove("col-12");
    document.getElementById("alwaysOnMenu").classList.add("col-5");
    document.getElementById("userForm").classList.remove("col-0");
    document.getElementById("userForm").classList.add("col-7");
    document.getElementById("userForm").style.display = "block";
}

// cancel the above changes and delete any potential values sent to the dateObj object
function notVisible() {
    document.getElementById("alwaysOnMenu").classList.remove("col-5");
    document.getElementById("alwaysOnMenu").classList.add("col-12");
    document.getElementById("userForm").classList.remove("col-7");
    document.getElementById("userForm").classList.add("col-0");
    document.getElementById("userForm").style.display = "none";
    document.getElementById("month").innerHTML = "Select The Month";
    document.getElementById("day").innerHTML = "Select The Day";
    document.getElementById("validationName").value = "";
    document.getElementById("validationDepartment").value = "";
    document.getElementsByClassName("date")[0].value = "";
    dateObj.month = ""
    dateObj.day = ""
    document.getElementsByClassName("date")[0].style.display = "none";
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
// only if the value is a positive number, else return a span html element
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

// call the addDate function with the month value
function visibleMonth(month) {
    document.getElementById("month").innerHTML = month;
    addDate(month, visibleMonth)
}

// call the addDate function with the day value
function visibleDay(i){
    document.getElementById("day").innerHTML = i;
    addDate(i, visibleDay)
}

// if both the month and day values in the dateObj object are populated
// add the values in a final date form
function visibleDate(){
    document.getElementsByClassName("date")[0].value = date;
    document.getElementsByClassName("date")[0].style.display = "block";
    document.getElementById("validationDate2").value = date;
}

// verifi what function called the addDate() and add the appropiate value in the dateObj object
function addDate(value, callerFunction) {
    if (callerFunction == visibleMonth) {
        dateObj.month = value;
        console.log("The value " + value + " has been added to the month.")
    } else {
        dateObj.day = value;
        console.log("The value " + value + " has been added to the day.")
    }

    if (dateObj.day !== "" && dateObj.month !== "") {
        date = dateObj.month + "-" + dateObj.day
        visibleDate()
    }
}


// bootstrap generated function
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