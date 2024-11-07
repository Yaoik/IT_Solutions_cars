$(document).ready(function() {
    url = $('input[name=car_update_url]').val()
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        headers: {
            'Authorization': localStorage.getItem('Token')
        },
        success: function(response) {
            $('#car-list').empty();
            $.each([response], function(index, car) {
                var carHtml = `<div class="w-64 h-32 border">`;
                carHtml += '<h3>' + car.make + ' ' + car.model + ' (Год: ' + (car.year ? car.year : 'Не указан') + ')</h3>';
                carHtml += '<p><strong>Описание:</strong> ' + car.description + '</p>';
                carHtml += '<p><strong>Владелец:</strong> ' + car.owner + '</p>';
                carHtml += '</div>';

                $('#car-detail').append(carHtml);
            });
        },
        error: function(xhr) {
            console.log('(')
        }
    });
    $('#editButton').click(function(e) {
        url = $('input[name=car_update_url]').val()
        e.preventDefault();

        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        var formData = {
            make: $('#make').val(),
            model: $('#model').val(),
            year: $('#year').val(),
            description: $('#description').val(),
        };
        for (i in formData) {
            if (formData[i] == ''){delete formData[i]}
        }
        $.ajax({
            url: url,
            type: 'PATCH',
            dataType: 'json',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            success: function(response) {
                window.location.reload()
            },
            error: function(xhr) {
                var errors;
                try {
                    errors = JSON.parse(xhr.responseText);
                } catch (e) {
                    errors = xhr.responseText;
                }
                var errorMessages = '';
                if (typeof errors === 'string') {
                    errorMessages += '<p style="color: red;">' + errors + '</p>';
                }
                else if (typeof errors === 'object' && errors !== null) {
                    $.each(errors, function(field, messages) {
                        if (Array.isArray(messages)) {
                            $.each(messages, function(index, message) {
                                errorMessages += '<p style="color: red;">Ошибка: ' + field + ' -> ' + message + '</p>';
                            });
                        } else {
                            errorMessages += '<p style="color: red;">Ошибка: ' + field + ' -> ' + messages + '</p>';
                        }
                    });
                }
                $('#responseMessage').html(errorMessages);
            }
        });
    });
});