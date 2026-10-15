document.addEventListener("DOMContentLoaded", () => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    document.querySelectorAll("[data-cyl]").forEach((root) => {
        const verbs = root.querySelector('[data-drum="v"]');
        const nouns = root.querySelector('[data-drum="n"]');
        if (!verbs || !nouns) return;
        const state = new Map([[verbs, 0], [nouns, 0]]);

        const turn = (drum) => {
            const n = state.get(drum) + 1;
            state.set(drum, n);
            drum.style.setProperty("--n", n);
            drum.querySelectorAll(".cw").forEach((word, i) => {
                word.dataset.k = (((i - n) % 5) + 5) % 5;
            });
        };

        let tick = 0;
        const timer = setInterval(() => {
            turn(tick % 2 === 0 ? verbs : nouns);
            tick += 1;
        }, 2300);
        document.addEventListener("visibilitychange", () => {
            if (document.hidden) clearInterval(timer);
        }, { once: true });
    });
});
