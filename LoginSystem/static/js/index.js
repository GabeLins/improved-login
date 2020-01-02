particlesJS('particles', {
    particles: {
        number: {
            value: 40,
            density: {
                enable: true,
                value_area: 500
            }
        },
        color: {
            value: '#ffffff'
        },
        shape: {
            type: 'circle',
        },
        opacity: {
            value: 0.5,
            random: true,
            anim: {
                enable: true,
                speed: 10,
                opacity_min: 0.2,
                sync: false
            }
        },
        size: {
            value: 5,
            random: true,
            anim: {
                enable: true,
                speed: 10,
                size_min: 1,
                sync: false
            }
        },
        line_linked: {
            enable: true,
            distance: 200,
            color: '#ffffff',
            opacity: 0.6,
            width: 1
        },
        move: {
            enable: true,
            speed: 5,
            direction: 'right',
            random: true,
            straight: false,
            out_mode: 'out',
        }
    },
    interactivity: {
        detect_on: 'window',
        events: {
            onhover: {
                enable: false,
            },
            onclick: {
                enable: false,
            },
            resize: false
        }
    },
    retina_detect: true
});

function verify_register () {
    const firstName = document.getElementById('first-name'),
          lastName = document.getElementById('last-name'),
          username = document.getElementById('username'),
          password = document.getElementById('password'),
          confirm = document.getElementById('confirm'),
          email = document.getElementById('email');
    
    firstName.addEventListener('input', () => {
        $err_name.innerHTML = '';
    }, { once: true });

    lastName.addEventListener('input', () => {
        $err_last.innerHTML = '';
    }, { once: true });

    username.addEventListener('input', () => {
        $err_user.innerHTML = '';
    }, { once: true });

    confirm.addEventListener('input', () => {
        $err_pass.innerHTML = '';
    }, { once: true });

    email.addEventListener('input', () => {
        $err_mail.innerHTML = '';
    }, { once: true });

    password.addEventListener('input', () => {
        if ( password.value.length < 8 ) return;
        $err_leng.innerHTML = '';
    });
}

if ( window.location.pathname === '/register' ) {
    verify_register();
}