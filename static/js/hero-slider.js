document.addEventListener("DOMContentLoaded", () => {
    const root = document.querySelector("[data-hero-slider]");
    if (!root) return;

    const slides = Array.from(root.querySelectorAll("[data-slide]"));
    const counter = root.querySelector("[data-slide-counter]");
    const dots = Array.from(root.querySelectorAll("[data-slide-dot]"));
    if (!slides.length) return;

    let index = 0;
    let timer = null;

    const show = (next) => {
        slides[index].classList.remove("is-active", "slide-flip");
        dots[index]?.classList.remove("is-active");
        index = (next + slides.length) % slides.length;
        const slide = slides[index];
        slide.classList.add("is-active");
        // force reflow so the animation restarts every time
        void slide.offsetWidth;
        slide.classList.add("slide-flip");
        dots[index]?.classList.add("is-active");
        if (counter) {
            counter.textContent = `0${index + 1} / 0${slides.length}`;
        }
    };

    const restart = () => {
        clearInterval(timer);
        timer = setInterval(() => show(index + 1), 4000);
    };

    root.querySelector("[data-slide-prev]")?.addEventListener("click", () => {
        show(index - 1);
        restart();
    });
    root.querySelector("[data-slide-next]")?.addEventListener("click", () => {
        show(index + 1);
        restart();
    });
    dots.forEach((dot, i) => {
        dot.addEventListener("click", () => {
            show(i);
            restart();
        });
    });

    show(0);
    restart();
});
