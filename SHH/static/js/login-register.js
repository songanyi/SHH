function showRegisterForm() {
    $('.loginBox').fadeOut('fast', function () {
        $('.registerBox').fadeIn('fast');
        $('.login-footer').fadeOut('fast', function () {
            $('.register-footer').fadeIn('fast');
        });
        $('.modal-title').html('Register');
    });
    $('.error').removeClass('alert alert-danger').html('');

}
function showLoginForm() {
    $('#loginModal .registerBox').fadeOut('fast', function () {
        $('.loginBox').fadeIn('fast');
        $('.register-footer').fadeOut('fast', function () {
            $('.login-footer').fadeIn('fast');
        });

        $('.modal-title').html('Sign In');
    });
    $('.error').removeClass('alert alert-danger').html('');
}

function openLoginModal() {
    showLoginForm();
    setTimeout(function () {
        $('#loginModal').modal('show');
    }, 230);
}
function openRegisterModal() {
    showRegisterForm();
    setTimeout(function () {
        $('#loginModal').modal('show');
    }, 230);

}

//obsolete
function registerAjax() {
    $.ajax({
        url: $(this).attr('action'),
        type: 'post',
        data: {
            username: $('useranme').val(),
            email: $('#username').val(),
            password1: $('#password1').val(),
            password2: $('#password2').val(),
        },
        success: function(data) {
            if (data.success) {
                // TODO to profile or something
                window.location.replace('/index/');
            } else {
                console.log(data);
                // TODO show errors accodring to data
                shakeModalRegister()
            }
        }
    });
}

function loginAjax() {
    //https://stackoverflow.com/questions/10041496/how-to-use-jquery-ajax-to-my-forms-action
    console.log($('#login-form').serialize());
    console.log("loginAjax", $("#login-form").attr('action'), $('#username-login').val(),  $('#password-login').val(), '{{ csrf_token }}');
    $.ajax({
        url: $("#login-form").attr('action'),
        type: 'POST',
        data: $('#login-form').serialize(),
        /*
        data: {
            'email': $('#email-login').val(),
            'password': $('#password-login').val(),
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']"),
            //stayloggedin: document.getElementById('stayloggedin').checked,
            //next: next,
        },
        */
        success: function(data) {
            console.log(data);
            if (data.success) {
                window.location.replace("/index/");
            } else {
                console.log(data);
                // TODO show errors accodring to data
                shakeModal()
            }
        }
    });
    /*   Simulate error message from the server   */
    //     shakeModal();
}

function shakeModal() {
    $('#loginModal .modal-dialog').addClass('shake');
    $('.error').addClass('alert alert-danger').html("Invalid email/password combination");
    $('input[type="password"]').val('');
    setTimeout(function () {
        $('#loginModal .modal-dialog').removeClass('shake');
    }, 1000);
}

function shakeModalRegister() {
    $('#loginModal .modal-dialog').addClass('shake');
    $('.error').addClass('alert alert-danger').html("Failed to register");
    $('input[type="password"]').val('');
    setTimeout(function () {
        $('#loginModal .modal-dialog').removeClass('shake');
    }, 1000);
}
