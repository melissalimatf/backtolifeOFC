$(document).ready(function () {
    // Registro de usuário
    $("#registerForm").on("submit", function (e) {
        e.preventDefault(); // Impede o comportamento padrão do formulário

        const formData = $(this).serialize(); // Serializa os dados do formulário

        $.ajax({
            url: "/register",
            type: "POST",
            data: formData,
            success: function (response) {
                alert(response.message); // Mostra a mensagem de sucesso
                window.location.href = response.redirect_url; // Redireciona para a página de login
            },
            error: function (xhr) {
                const error = xhr.responseJSON?.error || "Erro no servidor";
                alert(`Erro: ${error}`); // Mostra a mensagem de erro
            }
        });
    });

    // Login do usuário
    $("#login-form").on("submit", function (e) {
        e.preventDefault(); // Impede o comportamento padrão do formulário

        const formData = $(this).serialize(); // Serializa os dados do formulário

        $.ajax({
            url: "/login",
            type: "POST",
            data: formData,
            success: function (response) {
                console.log("Resposta recebida:", response);
                alert(response.message); // Mostra a mensagem de sucesso
                // Redireciona para a página do perfil retornada pelo backend
                window.location.href = response.redirect_url; 
            },
            error: function (xhr) {
                console.log("Erro recebido:", xhr.responseJSON);
                const error = xhr.responseJSON?.error || "Erro no servidor";
                alert(`Erro: ${error}`); // Mostra a mensagem de erro
            }
        });
    });
});
