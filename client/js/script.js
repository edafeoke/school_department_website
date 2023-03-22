const toggleButton = document.querySelector(".toggle-btn");
const toggleIcon = document.querySelector(".toggle-btn i");
const dropDownMenu = document.querySelector(".dropdown-menu");
const navbar = document.querySelector('nav')
let isOpen;

toggleButton.addEventListener("click", () => {
  dropDownMenu.classList.toggle("open");
  isOpen = dropDownMenu.classList.contains("open");

  toggleButton.innerHTML = isOpen
    ? '<i class="fa-solid fa-xmark"></i>'
    : '<i class="fa-solid fa-bars"></i>';
});



//Header Animation

const changeHeaderBackground = ()=>{
  let scrollValue = window.scrollY
  // console.log(scrollValue);
  if (scrollValue > 100) {
    navbar.classList.add('nav-dark');
  }else{
    navbar.classList.remove('nav-dark');
  }
}
window.addEventListener('scroll', changeHeaderBackground);