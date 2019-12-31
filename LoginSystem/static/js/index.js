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
