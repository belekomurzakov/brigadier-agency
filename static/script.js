let menu;
let toggle;

let slideshow, slideshowTitle;
let currentSlideIndex = -1;
const slides = [
    {
        image: 'software_engineer.jpeg',
    },
    {
        image: 'system_engineer.png',
    },
    {
        image: 'power_engineer.jpeg',
    },
];

function initializeMenu() {
    toggle = document.getElementById("menu-toggle");
    menu = document.getElementById("menu");

    toggle.addEventListener('click', toggleMenu);
}

function toggleMenu() {
    const isVisible = menu.classList.contains("expanded");

    if (isVisible) {
        menu.classList.remove('expanded');
    } else {
        menu.classList.add('expanded');
    }
}

function initializeSlideshow() {
    const leftArrow = document.getElementById("slideshow-left");
    const rightArrow = document.getElementById("slideshow-right");
    slideshow = document.getElementById("slideshow");
    //slideshowTitle = document.getElementById("slideshow-title");

    if (leftArrow && rightArrow) {
        leftArrow.addEventListener('click', () => moveSlide(-1));
        rightArrow.addEventListener('click', () => moveSlide(+1));
    }
}

function moveSlide(direction) {
    if (!slideshow) {
        return;
    }

    currentSlideIndex += direction;
    if (currentSlideIndex < 0) {
        currentSlideIndex = slides.length - 1;
    } else if (currentSlideIndex >= slides.length) {
        currentSlideIndex = 0;
    }

    const slide = slides[currentSlideIndex];

    slideshow.style.backgroundImage = `url("static/images/${slide.image}")`;
    // slideshowTitle.innerText = slide.title;
}

// main
document.addEventListener("DOMContentLoaded", () => {
    initializeMenu();
    initializeSlideshow();
    moveSlide(1);
});