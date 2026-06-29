const sidebar = document.getElementById("sidebar");

const menuButton = document.getElementById("menuButton");

menuButton.addEventListener("click", () => {

sidebar.classList.toggle("open");

});

const modal = document.getElementById("modal");

const openModal = document.getElementById("popularButton");

const closeModal = document.getElementById("closeModal");

const openModalMenu = document.getElementById("popularMenu");

function showModal(){

modal.classList.add("show");

}

openModal.addEventListener("click", showModal);

openModalMenu.addEventListener("click", showModal);

closeModal.addEventListener("click", ()=>{

modal.classList.remove("show");

});

modal.addEventListener("click",(e)=>{

if(e.target===modal){

modal.classList.remove("show");

}

});

const search = document.getElementById("search");

const items = document.querySelectorAll(".book-item");

search.addEventListener("input",function(){

const value = this.value.toLowerCase();

items.forEach(item=>{

const text = item.textContent.toLowerCase();

if(text.includes(value)){

item.style.display="block";

}else{

item.style.display="none";

}

});

});