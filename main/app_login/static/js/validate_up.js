function validateForm(event) {
    const usernameField = document.querySelector('#username');
    const emailField = document.querySelector('#email-address');
    const passwordField = document.querySelector('#password');
    const confirmField = document.querySelector('#confirm-password');
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    let isInvalid = false;

    // Resetando o estilo inicial dos campos
    resetFieldStyles([usernameField, emailField, passwordField, confirmField]);
    
    // Validação de username
    if (usernameField.value.length < 5) {
        setFieldError(usernameField, 'Username must be more than 5 characters');
        isInvalid = true;
    }

    // Validação de email
    if (!emailPattern.test(emailField.value)) {
        setFieldError(emailField, 'Invalid email');
        isInvalid = true;
    }
    
    // Validação de senha
    if (passwordField.value.length < 8) {
        setFieldError(passwordField, 'Password must be more than 8 characters');
        confirmField.value = '';
        isInvalid = true;
    } else {
        // Validação de confirmar senha
        if (passwordField.value !== confirmField.value) {
            setFieldError(confirmField, 'Password does not match');
            isInvalid = true;
    }
    }
    
    if (isInvalid) {
        event.preventDefault();
    }
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
    field.style.borderColor = 'red';
    field.value = '';
    field.setAttribute('placeholder', errorMessage);
}
