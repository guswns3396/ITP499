let name = document.querySelector("#name-id");
let pw = document.querySelector("#pw-id");

let form = document.querySelector("form")

let valid_name = false;
let valid_pw = false;

console.log(name);
console.log(pw);
console.log(form);

form.onsubmit = function(event) {
	event.preventDefault();
	// console.log("prevented");

	if (!name.value) {
		valid_name = false;
		name.nextElementSibling.classList.remove("hidden");
	}
	else {
		valid_name = true;
		name.nextElementSibling.classList.add("hidden");
	}
	if (!pw.value) {
		valid_pw = false;
		pw.nextElementSibling.classList.remove("hidden");
	}
	else {
		valid_pw = true;
		pw.nextElementSibling.classList.add("hidden");
	}
	if (valid_name && valid_pw) {
		document.querySelector("form").submit();
	}
}
