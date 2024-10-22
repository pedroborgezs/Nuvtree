function validateForm(event) {
    const usernameField = document.querySelector('#username');
    const numberField = document.querySelector('#phone-number');
    const passwordField = document.querySelector('#password');
    const confirmField = document.querySelector('#confirm-password');
    
    let isInvalid = false;

    // Resetando o estilo inicial dos campos
    resetFieldStyles([usernameField, numberField, passwordField, confirmField]);
    
    // Validação de username
    if (usernameField.value.length < 5) {
        setFieldError(usernameField, 'Username must be more than 5 characters');
        isInvalid = true;
    }

    // Validação de número de telefone
    const phonePattern = /^\d{11}$/;
    if (!phonePattern.test(numberField.value)) {
        setFieldError(numberField, 'Telephone number must contain exactly 11 digits');
        isInvalid = true;
    }

    // Validação de senha
    if (passwordField.value.length < 8) {
        setFieldError(passwordField, 'Password must be more than 8 characters');
        confirmField.value = '';
        isInvalid = true;
    } else {
        // Validação de confirmação de senha
        if (passwordField.value !== confirmField.value) {
            setFieldError(confirmField, 'Password does not match');
            isInvalid = true;
        }
    }

    // Se algum campo for inválido, impede o envio do formulário
    if (isInvalid) {
        event.preventDefault(); // Impede o envio do formulário
        return false; // Garante que a função retorne false
    }

    return true; // Se tudo estiver correto, permite o envio do formulário
}

function resetFieldStyles(fields) {
    fields.forEach(field => {
        field.addEventListener('focus', () => {
            field.style.borderColor = ''; // Reseta a cor da borda para o padrão
            field.setAttribute('placeholder', field.id.charAt(0).toUpperCase() + field.id.slice(1)); // Restaura o placeholder
        });
    });
}

function setFieldError(field, errorMessage) {
    field.style.borderColor = 'red'; // Define a borda do campo como vermelha
    field.value = ''; // Limpa o valor do campo
    field.setAttribute('placeholder', errorMessage); // Exibe a mensagem de erro no placeholder
}
