$(document).ready(function() {
    url = $('input[name=car_url]').val()
    console.log(url)
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
                var carHtml = '<div class="w-64 h-32 border ">';
                carHtml += '<h3>' + car.make + ' ' + car.model + ' (Год: ' + (car.year ? car.year : 'Не указан') + ')</h3>';
                carHtml += '<p><strong>Описание:</strong> ' + car.description + '</p>';
                carHtml += '<p><strong>Владелец:</strong> ' + car.owner + '</p>';
                carHtml += '</div>';

                $('#car-list').append(carHtml);
            });
        },
        error: function(xhr) {
            console.log('(')
        }
    });
});