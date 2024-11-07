$(document).ready(function() {
    url = $('input[name=car_url]').val()
    detail_url = $('input[name=car_url]').data('car')
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
            $.each(response, function(index, car) {
                var carHtml = `<a class="w-64 border hover:bg-slate-200" href="${detail_url.replace('0', car.id)}">`;
                carHtml += '<h3>' + car.make + ' ' + car.model + ' (Год: ' + (car.year ? car.year : 'Не указан') + ')</h3>';
                carHtml += '<p><strong>Описание:</strong> ' + car.description + '</p>';
                carHtml += '<p><strong>Владелец:</strong> ' + car.owner + '</p>';
                carHtml += '</a>';

                $('#car-list').append(carHtml);
            });
        },
        error: function(xhr) {
            console.log('(')
        }
    });
    $('#createButton').click(function(e) {
        e.preventDefault();

        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        var url = $('button[name="createButton"]').data('url');

        var formData = {
            make: $('#make').val(),
            model: $('#model').val(),
            year: $('#year').val(),
            description: $('#description').val(),
        };
        if (formData['year'] == ''){
            delete(formData['year'])
        }
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