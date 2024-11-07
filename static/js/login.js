$(document).ready(function() {
    $('#loginButton').click(function(e) {
        e.preventDefault();

        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        var url = $('button[name="loginButton"]').data('url');

        var formData = {
            email: $('#email').val(),
            password: $('#password').val(),
        };

        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function(response) {
                $('#responseMessage').html('<p style="color: green;">' + response.message + '</p>');
                localStorage.setItem('Token', 'Token ' + response.token)
                window.location.href = $('button[name="loginButton"]').data('redirect')
            },
            error: function(xhr) {
                var errors = JSON.parse(xhr.responseText);
                var errorMessages = '';

                $.each(errors, function(field, messages) {
                    $.each(messages, function(index, message) {
                        errorMessages += '<p style="color: red;">Ошибка: ' + field + ' -> ' + message + '</p>';
                    });
                });
            
                $('#responseMessage').html(errorMessages);
            }
        });
    });
});