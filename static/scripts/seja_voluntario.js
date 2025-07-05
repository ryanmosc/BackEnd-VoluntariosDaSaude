document.addEventListener('DOMContentLoaded', () => {
  // ============ 1. ANIMAÇÃO DO TÍTULO ============
  gsap.from(".formulario-titulo", {
    duration: 1,
    y: 50,
    opacity: 0,
    ease: "back.out(1.7)",
    delay: 0.3
  });

  // ============ 2. ANIMAÇÃO DOS ELEMENTOS DO FORMULÁRIO ============
  const formElements = document.querySelectorAll(".formulario-voluntario *:not(button)");

  gsap.from(formElements, {
    duration: 0.8,
    y: 30,
    opacity: 0,
    stagger: 0.15,
    ease: "power2.out",
    scrollTrigger: {
      trigger: ".formulario-voluntario",
      start: "top 80%"
    }
  });

  // ============ 3. ANIMAÇÃO DO BOTÃO ============
  gsap.from(".botao-enviar", {
    duration: 1,
    scale: 0.8,
    opacity: 0,
    ease: "elastic.out(1, 0.5)",
    scrollTrigger: {
      trigger: ".botao-enviar",
      start: "top 90%"
    }
  });

  // Efeito hover no botão
  const submitBtn = document.querySelector(".botao-enviar");

  submitBtn.addEventListener("mouseenter", () => {
    gsap.to(submitBtn, {
      duration: 0.3,
      scale: 1.05,
      boxShadow: "0 5px 15px rgba(0,0,0,0.2)",
      ease: "power2.out"
    });
  });

  submitBtn.addEventListener("mouseleave", () => {
    gsap.to(submitBtn, {
      duration: 0.3,
      scale: 1,
      boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      ease: "power2.out"
    });
  });

  // ============ 4. ANIMAÇÃO DURANTE O ENVIO ============
  document.querySelector(".formulario-voluntario").addEventListener("submit", function (e) {
    e.preventDefault();

    const btn = this.querySelector(".botao-enviar");
    const originalText = btn.textContent;


    gsap.to(btn, {
      duration: 0.3,
      backgroundColor: "#4CAF50",
      color: "white",
      onComplete: () => {
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';


        setTimeout(() => {
          btn.innerHTML = '<i class="fas fa-check"></i> Enviado!';


          setTimeout(() => {
            gsap.to(btn, {
              duration: 0.3,
              backgroundColor: "",
              color: "",
              onComplete: () => {
                btn.textContent = originalText;
              }
            });
          }, 2000);
        }, 1500);
      }
    });
  });
});

//======= 5. INTEGRAÇÃO COM A API =======

document.getElementById('seja-voluntario-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const data = {
    nome: formData.get('nome'),
    email: formData.get('email'),
    telefone: formData.get('telefone'),
    disponibilidade: formData.get('disponibilidade'),
    mensagem: formData.get('mensagem')
  };
  const messageDiv = document.getElementById('form-message');
  const submitButton = form.querySelector('.botao-enviar');
  messageDiv.style.display = 'none';
  messageDiv.style.color = '#333';
  submitButton.textContent = 'Enviando...';
  submitButton.disabled = true;

  try {
    const response = await fetch('/api/seja_voluntario', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const result = await response.json();
    if (response.ok) {
      messageDiv.style.display = 'block';
      messageDiv.style.color = 'green';
      messageDiv.textContent = 'Cadastro enviado com sucesso!';
      form.reset();
    } else {
      messageDiv.style.display = 'block';
      messageDiv.style.color = 'red';
      messageDiv.textContent = result.error || 'Erro ao enviar o cadastro.';
    }
  } catch (error) {
    messageDiv.style.display = 'block';
    messageDiv.style.color = 'red';
    messageDiv.textContent = 'Erro ao conectar com o servidor.';
  } finally {
    submitButton.textContent = 'Enviar Cadastro';
    submitButton.disabled = false;
  }
});