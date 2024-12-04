const tabs = document.querySelectorAll('.tab');
const contents = document.querySelectorAll('.form-content');
const clientTypeRadios = document.querySelectorAll('input[name="clientType"]');
const rehabFields = document.getElementById('rehabFields');
const educationFields = document.getElementById('educationFields');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const target = tab.getAttribute('data-target');
        contents.forEach(content => {
            content.classList.remove('active');
            if (content.id === target) {
                content.classList.add('active');
            }
        });
    });
});

clientTypeRadios.forEach(radio => {
    radio.addEventListener('change', () => {
        rehabFields.classList.add('hidden');
        educationFields.classList.add('hidden');

        if (radio.value === 'rehab') rehabFields.classList.remove('hidden');
        if (radio.value === 'education') educationFields.classList.remove('hidden');
    });
});

const areaForm = document.querySelector('.area-form');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const target = tab.getAttribute('data-target');
        contents.forEach(content => {
            content.classList.remove('active');
            if (content.id === target) {
                content.classList.add('active');
            }
        });

        // Ajustar padding com base na aba ativa
        if (target === 'login-form') {
            areaForm.classList.add('login-active');
        } else {
            areaForm.classList.remove('login-active');
        }
    });
});
// Alternar entre abas (Cadastro/Login)
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        const target = tab.getAttribute('data-target');
        contents.forEach(content => {
            content.classList.remove('active');
            if (content.id === target) {
                content.classList.add('active');
            }
        });

        // Redefinir campos ao alternar para login
        if (target === 'login-form') {
            resetLoginForm();
        }
    });
});

// Função para gerenciar "Esqueceu a senha?"
document.getElementById('forget-password').addEventListener('click', function () {
    areaForm.classList.add('login-activeForget');
    document.getElementById('password-group').style.display = 'none'; // Esconde senha
    document.getElementById('recover-title').style.display = 'block'; // Exibe "Recuperar Senha"
    document.getElementById('submit-button').innerText = 'Enviar E-mail'; // Muda botão
});

// Função para redefinir o formulário de login
function resetLoginForm() {
    // Mostrar grupo de senha
    document.getElementById('password-group').style.display = 'block';

    // Esconder título de recuperação
    document.getElementById('recover-title').style.display = 'none';

    // Restaurar texto do botão
    document.getElementById('submit-button').innerText = 'Entrar';
}
