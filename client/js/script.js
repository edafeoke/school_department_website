const toggleButton = document.querySelector(".toggle-btn");
const toggleIcon = document.querySelector(".toggle-btn i");
const dropDownMenu = document.querySelector(".dropdown-menu");

let isOpen;

toggleButton.addEventListener("click", () => {
  dropDownMenu.classList.toggle("open");
  isOpen = dropDownMenu.classList.contains("open");

  toggleButton.innerHTML = isOpen
    ? '<i class="fa-solid fa-xmark"></i>'
    : '<i class="fa-solid fa-bars"></i>';
});

// document.querySelector('.content').addEventListener('click',()=>{
//   if(isOpen)  {
//     dropDownMenu.classList.toggle("open");
//   }

// })

//Header Animation
const header = document.querySelector("header");

let i = 1;

const slideShow = () => {
  setInterval(() => {
    if (i == 1) {
      header.classList.remove("header-back-3");
      header.classList.add("header-back-1");
      i = 2;
    } else if (i == 2) {
      header.classList.remove("header-back-1");
      header.classList.add("header-back-2");
      i = 3;
    } else {
      header.classList.remove("header-back-2");
      header.classList.add("header-back-3");
      i = 1;
    }
  }, 5000);
};
document.onload = slideShow();
