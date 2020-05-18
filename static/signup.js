let fname = document.querySelector("#fname-id");
let lname = document.querySelector("#lname-id");
let email = document.querySelector("#email-id");
let name = document.querySelector("#name-id");
let pw = document.querySelector("#pw-id");
let form = document.querySelector("form")

let valid_fname = false;
let valid_lname = false;
let valid_name = false;
let valid_pw = false;
let valid_email = false;

let PW_LENGTH = 7;

console.log(fname);
console.log(lname);
console.log(email);
console.log(name);
console.log(pw);
console.log(form);

form.onsubmit = function(event) {
	event.preventDefault();
	console.log("prevented");

	if (!fname.value) {
		valid_fname = false;
		fname.nextElementSibling.classList.remove("hidden");
	}
	else {
		valid_fname = true;
		fname.nextElementSibling.classList.add("hidden");
	}
	if (!lname.value) {
		valid_lname = false;
		lname.nextElementSibling.classList.remove("hidden");
	}
	else {
		valid_lname = true;
		lname.nextElementSibling.classList.add("hidden");
	}
	if (!name.value) {
		valid_name = false;
		name.nextElementSibling.classList.remove("hidden");
	}
	else {
		valid_name = true;
		name.nextElementSibling.classList.add("hidden");
	}
	if (pw.value.length < PW_LENGTH) {
		valid_pw = false;
		pw.nextElementSibling.classList.remove("hidden");
	}
	else {
		valid_pw = true;
		pw.nextElementSibling.classList.add("hidden");
	}
	if (!email.value.includes("@")) {
		valid_email = false;
		email.nextElementSibling.classList.remove("hidden");
	}
	else {
		valid_email = true;
		email.nextElementSibling.classList.add("hidden");
	}
	if (valid_name && valid_pw && valid_email) {
		// console.log("success");
		document.querySelector("form").submit();
	}
}
