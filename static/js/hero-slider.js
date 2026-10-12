document.addEventListener("DOMContentLoaded", () => {
    const root = document.querySelector("[data-hero-slider]");
    if (!root) return;

    const slides = Array.from(root.querySelectorAll("[data-slide]"));
    const dots = Array.from(root.querySelectorAll("[data-slide-dot]"));
    const counter = root.querySelector("[data-slide-counter]");
    if (!slides.length) return;

    const INTERVAL = 5000;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const pad = (n) => String(n).padStart(2, "0");
    let index = 0;
    let timer = null;

    const show = (next) => {
        slides[index].classList.remove("is-active");
        dots[index]?.classList.remove("is-active");
        index = (next + slides.length) % slides.length;
        slides[index].classList.add("is-active");
        dots[index]?.classList.add("is-active");
        dots.forEach((dot, i) => dot.setAttribute("aria-current", i === index ? "true" : "false"));
        if (counter) counter.textContent = `${pad(index + 1)} / ${pad(slides.length)}`;
    };

    const stop = () => {
        clearInterval(timer);
        timer = null;
    };

    const start = () => {
        stop();
        if (reduceMotion || slides.length < 2) return;
        timer = setInterval(() => show(index + 1), INTERVAL);
    };

    const go = (next) => {
        show(next);
        start();
    };

    root.querySelector("[data-slide-prev]")?.addEventListener("click", () => go(index - 1));
    root.querySelector("[data-slide-next]")?.addEventListener("click", () => go(index + 1));
    dots.forEach((dot, i) => dot.addEventListener("click", () => go(i)));

    root.addEventListener("mouseenter", stop);
    root.addEventListener("mouseleave", start);
    root.addEventListener("focusin", stop);
    root.addEventListener("focusout", start);
    document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));

    let touchX = null;
    root.addEventListener("touchstart", (e) => (touchX = e.touches[0].clientX), { passive: true });
    root.addEventListener("touchend", (e) => {
        if (touchX === null) return;
        const dx = e.changedTouches[0].clientX - touchX;
        touchX = null;
        if (Math.abs(dx) > 40) go(index + (dx < 0 ? 1 : -1));
    });

    show(0);
    start();
});
