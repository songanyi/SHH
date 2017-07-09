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

function loginAjax() {
    /*
    $.post("/accounts/login/", function (data) {
        if (data == 1) {
            window.location.replace("/index");
        } else {
            shakeModal();
        }
    });
    */

    $.ajax({
        url: '/accounts/login',
        type: 'post',
        data: {
            email: $('#email-login').val(),
            password: $('#password-login').val(),
            //stayloggedin: document.getElementById('stayloggedin').checked,
            next: next,
        },
        success: function(data) {
            if (data.success) {
                window.location.replace("/index");
            } else {
                console.log(data);
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

