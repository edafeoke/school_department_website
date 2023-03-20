const toggleButton = document.querySelector(".toggle-btn");
const toggleIcon = document.querySelector(".toggle-btn i");
const dropDownMenu = document.querySelector(".dropdown-menu");

let isOpen;

toggleButton.addEventListener("click", () => {
  dropDownMenu.classList.toggle("open");
  isOpen = dropDownMenu.classList.contains("open");

  toggleButton.innerHTML = isOpen ? '<i class="fa-solid fa-xmark"></i>' : '<i class="fa-solid fa-bars"></i>';
});

// document.querySelector('.content').addEventListener('click',()=>{
//   if(isOpen)  {
//     dropDownMenu.classList.toggle("open");
//   }


// })