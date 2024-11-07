$(document).ready(function() {
    url = $('input[name=comments_url]').val()
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        contentType: 'application/json',
        headers: {
            'Authorization': localStorage.getItem('Token')
        },
        success: function(response) {
            $('#comment-list').empty();
            $.each(response, function(index, comment) {
                var commentHtml = `<div class="min-w-64 border">`;
                commentHtml += '<h3>' + comment.author ;
                commentHtml += '<p><strong>Создан:</strong> ' + comment.created_at + '</p>';
                commentHtml += '<p><strong>Текст:</strong> ' + comment.content + '</p>';
                commentHtml += '</div>';

                $('#comment-list').append(commentHtml);
            });
        },
        error: function(xhr) {
            console.log('(')
        }
    });
    $('#create_comment').click(function(e) {
        url = $('input[name=comments_url]').val()
        e.preventDefault();

        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        var formData = {
            content: $('#content').val(),
        };
        for (i in formData) {
            if (formData[i] == ''){delete formData[i]}
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
                $('#responseMessage_comment').html(errorMessages);
            }
        });
    });
});