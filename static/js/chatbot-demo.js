// Chat de demostración: respuestas escritas a mano, sin servicio de IA detrás.
(function () {
  var root = document.querySelector("[data-chat]");
  if (!root) return;
  var log = root.querySelector("[data-log]");
  var chips = root.querySelectorAll("[data-chip]");
  var replies = {
    "Cotizar pintura de fachada": "Perfecto. Cuéntame qué tipo de edificio es y cuántos pisos tiene; un asesor te confirma el valor por WhatsApp.",
    "Impermeabilizar mi terraza": "Claro. ¿Ves filtraciones o humedad? Con eso coordinamos una visita técnica.",
    "Agendar una visita técnica": "Listo. Elige fecha y jornada en «Agenda tu cita» y te escribimos para confirmar.",
    "Conocer servicios": "Hacemos acabados (pintura, enlucido, estuco, yeso, revestimientos, vidriería) e instalaciones especializadas (aislamiento, sellado e impermeabilización)."
  };
  var busy = false;

  function bubble(text, mine) {
    var row = document.createElement("div");
    row.className = "flex" + (mine ? " justify-end" : "");
    var b = document.createElement("div");
    b.className = "max-w-[82%] px-5 py-3.5 text-lg leading-[1.4] lg:text-[22px] " +
      (mine ? "rounded-[24px_24px_4px_24px] bg-white text-[#1d1c1c]" : "rounded-[24px_24px_24px_4px] bg-[#dedede] text-[#1d1c1c]");
    b.textContent = text;
    row.appendChild(b);
    log.appendChild(row);
    while (log.scrollHeight > log.clientHeight && log.children.length > 1) log.removeChild(log.firstChild);
    return row;
  }
  function typing() {
    var d = document.createElement("div");
    d.className = "flex items-center gap-[7px] self-start rounded-[24px_24px_24px_4px] bg-[#dedede] px-5 py-4";
    d.innerHTML = [0, 0.18, 0.36].map(function (s) {
      return '<span class="h-[9px] w-[9px] rounded-full bg-[#8a8a8a]" style="animation:twDot 1.2s ' + s + 's infinite"></span>';
    }).join("");
    log.appendChild(d);
    return d;
  }
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      if (busy) return;
      busy = true;
      var q = chip.dataset.chip;
      bubble(q, true);
      var dots = typing();
      setTimeout(function () {
        dots.remove();
        bubble(replies[q], false);
        busy = false;
      }, 1400);
    });
  });
})();
