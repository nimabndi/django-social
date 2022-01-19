$('#following_btn').click(function () {

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


    var user_id = $('#following_btn').attr('data-id')
    var follow = $('#following_btn').text()

    if (follow == 'follow') {
        var url = '/account/follow/'
        var btn_text = 'unfollow'
        var btn_class = 'btn btn-warning text-center mx-auto'
    } else {
        var url = '/account/unfollow/'
        var btn_text = 'follow'
        var btn_class = 'btn btn-primary text-center mx-auto'
    }

    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'user_id': user_id,
        },
        success: function (data) {
            if (data['status'] == 'ok') {
                $('#following_btn').text(btn_text)
                $('#following_btn').attr({'class': btn_class})
            }

        }

    });

});