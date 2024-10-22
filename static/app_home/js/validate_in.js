function validateForm(event) {
    const numberField = document.querySelector('#phone-number');
    const passwordField = document.querySelector('#password');
    
    let isInvalid

    // Resetando o estilo inicial dos campos
    resetFieldStyles([numberField, passwordField]);
    
    // Validação de username
    const phonePattern = /^\d{11}$/;
    if (!phonePattern.test(numberField.value)) {
        setFieldError(phoneField, 'Telephone number must contain exactly 11 digits');
        isInvalid = True;
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
