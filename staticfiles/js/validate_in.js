function validateForm(event) {
    const emailField = document.querySelector('#email-address');
    const passwordField = document.querySelector('#password');
    
    let isInvalid

    // Resetando o estilo inicial dos campos
    resetFieldStyles([emailField, passwordField]);
    
    // Validação de username
    if (emailField.value.length < 5) {
        setFieldError(emailField, 'Invalid email');
        isInvalid = true;
    }
    
    // Validação de senha
    if (passwordField.value.length < 8) {
        setFieldError(passwordField, 'Invalid password');
        isInvalid = true;
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
