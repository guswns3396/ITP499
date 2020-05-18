let date = document.querySelector("#date-id");
let form = document.querySelector("form");

console.log(date);
console.log(form);

form.onsubmit = function(event) {
	event.preventDefault();
	// console.log("prevented");

	// console.log(date.value)
	let date0 = new Date("2020-03-22");


	if (date.value) {
		console.log("not null");
		let date1 = new Date(date.value);
		if (date1 > date0) {
			// alert("success");
			date.nextElementSibling.classList.add("hidden");
			document.querySelector("form").submit();
		}
		else {
			date.nextElementSibling.classList.remove("hidden");
		}
	}
	else {
		console.log("null");
		date.nextElementSibling.classList.remove("hidden");
	}
}
