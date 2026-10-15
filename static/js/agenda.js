// Vista previa en vivo del mensaje de WhatsApp (mismo formato que appointment_message en views.py)
(function () {
  var form = document.querySelector("[data-agenda]");
  if (!form) return;
  var preview = form.querySelector("[data-preview]");
  var word = document.querySelector("[data-modality-word]");

  function val(name) {
    var el = form.elements[name];
    if (!el) return "";
    if (el.length !== undefined && el.type === undefined) {
      for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value;
      return "";
    }
    return el.value.trim();
  }
  function fmt(d) {
    var p = d.split("-");
    return p[2] + "/" + p[1] + "/" + p[0];
  }
  function render() {
    var modality = val("modality") === "presencial" ? "Presencial" : "Virtual";
    var slot = val("preferred_slot") === "tarde" ? "Tarde" : "Mañana";
    var name = val("full_name"), phone = val("phone"), date = val("preferred_date");
    var lines = ["Hola Aplideco, quiero agendar una cita.", "Modalidad: " + modality];
    if (name) lines.push("Nombre: " + name);
    if (phone) lines.push("Teléfono: " + phone);
    lines.push("Servicio: " + val("service"));
    lines.push(date ? "Fecha preferida: " + fmt(date) + " (" + slot + ")" : "Jornada preferida: " + slot);
    preview.textContent = lines.join("\n");
    if (word) word.textContent = modality.toLowerCase();
  }
  form.addEventListener("input", render);
  form.addEventListener("change", render);
  render();
})();
