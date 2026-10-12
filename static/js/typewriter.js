document.addEventListener("DOMContentLoaded", () => {
    const TYPE_MS = 75;
    const ERASE_MS = 32;
    const HOLD_MS = 1700;
    const GAP_MS = 380;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    document.querySelectorAll("[data-typewriter]").forEach((el) => {
        let words;
        try {
            words = JSON.parse(el.dataset.words || "[]");
        } catch (e) {
            return;
        }
        if (!words.length) return;
        if (reduceMotion) {
            el.textContent = words[0];
            return;
        }

        let w = 0;
        let i = 0;
        let erasing = false;

        const tick = () => {
            const word = words[w];
            if (!erasing) {
                i += 1;
                el.textContent = word.slice(0, i);
                if (i === word.length) {
                    erasing = true;
                    return setTimeout(tick, HOLD_MS);
                }
                return setTimeout(tick, TYPE_MS + Math.random() * 50);
            }
            i -= 1;
            el.textContent = word.slice(0, i);
            if (i === 0) {
                erasing = false;
                w = (w + 1) % words.length;
                return setTimeout(tick, GAP_MS);
            }
            return setTimeout(tick, ERASE_MS);
        };

        setTimeout(tick, 600);
    });
});
