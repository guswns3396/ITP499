let rad = document.querySelector("#radius-id");
let form = document.querySelector("form");

console.log(rad)

form.onsubmit = function(event) {
	event.preventDefault();
	r = parseInt(rad.value, 10);
	if (r > 0) {
		rad.nextElementSibling.classList.add("hidden");
		form.submit();
	}
	else {
		rad.nextElementSibling.classList.remove("hidden");
	}
}