$('#like_dislike_btn').click(function () {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    var post_id = $('#like_dislike_btn').attr('data-id')
    var like = $('#like_dislike_btn').text()

    if (like == 'Like') {
        var url = '/account/like/'
        var btn_text = 'Dislike'
    } else {
        var url = '/account/dislike/'
        var btn_text = 'Like'
    }

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'post_id': post_id,
        },
        success: function (data) {
            if (data['status'] == 'ok') {
                $('#like_dislike_btn').text(btn_text)
            }

        }

    });

});