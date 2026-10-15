document.addEventListener("DOMContentLoaded", () => {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    document.querySelectorAll("[data-carousel]").forEach((root) => {
        const slides = Array.from(root.querySelectorAll("[data-slide]"));
        if (slides.length < 1) return;
        const dots = Array.from(root.querySelectorAll("[data-dot]"));
        const thumbs = Array.from(root.querySelectorAll("[data-thumb]"));
        const cap = root.querySelector("[data-cap-text]");
        const title = root.querySelector("[data-title-text]");
        const desc = root.querySelector("[data-desc-text]");
        const counter = root.querySelector("[data-counter]");
        const interval = parseInt(root.dataset.interval || "5200", 10);
        const stopOnClick = root.hasAttribute("data-stop-on-click");
        let index = 0;
        let timer = null;
        let stopped = false;

        const show = (next) => {
            index = (next + slides.length) % slides.length;
            const s = slides[index];
            slides.forEach((el, k) => {
                el.classList.toggle("is-active", k === index);
                el.setAttribute("aria-hidden", k === index ? "false" : "true");
                el.querySelectorAll("a").forEach((a) => (a.tabIndex = k === index ? 0 : -1));
            });
            dots.forEach((el, k) => el.setAttribute("aria-current", k === index ? "true" : "false"));
            thumbs.forEach((el, k) => el.setAttribute("aria-current", k === index ? "true" : "false"));
            if (cap) cap.textContent = s.dataset.cap || "";
            if (title) title.textContent = s.dataset.cap || "";
            if (desc) desc.textContent = s.dataset.desc || "";
            if (counter) counter.textContent = `${index + 1} / ${slides.length}`;
        };

        const pause = () => {
            clearInterval(timer);
            timer = null;
        };
        const play = () => {
            pause();
            if (reduceMotion || stopped || slides.length < 2) return;
            timer = setInterval(() => show(index + 1), interval);
        };
        const go = (next, manual) => {
            show(next);
            if (manual && stopOnClick) stopped = true;
            play();
        };

        root.querySelectorAll("[data-prev]").forEach((b) => b.addEventListener("click", () => go(index - 1, true)));
        root.querySelectorAll("[data-next]").forEach((b) => b.addEventListener("click", () => go(index + 1, true)));
        dots.forEach((el, k) => el.addEventListener("click", () => go(k, true)));
        thumbs.forEach((el, k) => el.addEventListener("click", () => go(k, true)));

        root.addEventListener("mouseenter", pause);
        root.addEventListener("mouseleave", play);
        root.addEventListener("focusin", pause);
        root.addEventListener("focusout", play);
        root.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft") go(index - 1, true);
            if (e.key === "ArrowRight") go(index + 1, true);
        });
        document.addEventListener("visibilitychange", () => (document.hidden ? pause() : play()));

        let touchX = null;
        root.addEventListener("touchstart", (e) => (touchX = e.touches[0].clientX), { passive: true });
        root.addEventListener("touchend", (e) => {
            if (touchX === null) return;
            const dx = e.changedTouches[0].clientX - touchX;
            touchX = null;
            if (Math.abs(dx) > 40) go(index + (dx < 0 ? 1 : -1), true);
        });

        show(0);
        play();
    });
});
