document.addEventListener('DOMContentLoaded', () => {
  const mailBtn = document.getElementById('btn-mail');  // Asegurate de que tu botón tenga id="btn-mail"

  if (mailBtn) {
    mailBtn.addEventListener('click', () => {
      const email = 'martincontarino2125@gmail.com';
      const subject = 'Consulta desde tu portfolio';
      const body = 'Hola Martín,\n\nVi tu portfolio y me copó el bot del dólar.\n\nNecesito algo así pero para...\n\nMi nombre es...\nMi presupuesto aproximado es...\n\nSaludos!';

      const mailtoLink = `mailto:${email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

      // Intenta abrir mailto
      window.location.href = mailtoLink;

      // Fallback: si no abre (chequea después de 2 seg si el foco cambió o algo)
      setTimeout(() => {
        if (document.hasFocus()) {  // Si el foco sigue en la página, probablemente no abrió
          // Copia al portapapeles
          navigator.clipboard.writeText(email).then(() => {
            alert('¡Copiado al portapapeles! Pegalo en Gmail o tu mail y escribime directo. Si seguís con dramas, DM en X @Martin_10_0_01   .');
          }).catch(() => {
            alert(`No pude copiar, pero escribime a: ${email}`);
          });
        }
      }, 2000);
    });
  }
});
// Inicializá EmailJS con tu Public Key
emailjs.init("jR5nJomhs4BnSTNPe");  // Reemplazá con la tuya real

document.getElementById('contact-form').addEventListener('submit', function(event) {
  event.preventDefault();  // Evita que recargue la página

  const params = {
    nombre: document.getElementById('nombre').value,
    email: document.getElementById('email').value,
    mensaje: document.getElementById('mensaje').value,
    subject: "Consulta desde portfolio"  // Podés dejar fijo o usar un input
  };

  emailjs.send("service_x9jl2u8", "template_28wt6yy", params)
    .then(() => {
      document.getElementById('status').innerHTML = "¡Mail enviado! Te respondo en cuanto pueda. Gracias por confiar en mí.";
      document.getElementById('status').style.color = "#00ff88";
      document.getElementById('contact-form').reset();  // Limpia el form
    }, (error) => {
      document.getElementById('status').innerHTML = "Algo salió para el orto: " + error.text + ". Probá de nuevo o escribime directo a martincontarino2125@gmail.com";
      document.getElementById('status').style.color = "#ff3366";
    });
});