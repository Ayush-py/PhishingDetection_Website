
const Button = document.querySelector(".noselect");
Button.addEventListener("click", () => {
label1 = document.getElementById('label1');
label1.innerHTML = ("Processing URL...");
label1.style.padding = '150px 0px 10px 75px';
Button.remove();

})
