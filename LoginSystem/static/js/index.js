$('#next').click(() => { 
    let pattern = /\S+@\S+\.\S+/;
    let address = $('#email').val();

    // Check if the entered email address is valid
    if ( !pattern.test(address) ) {
        $('#err_mail').text('Invalid Email');
        return;
    }
    $('#err_mail').text('');
    $('#address').text(address);

    // Move forwards to the next fieldset 
    $('#fieldset0').css('display', 'none');
    $('#fieldset1').css('display', 'initial');
});


$('#back').click(() => {
    // Move backwards to the previous fieldset
    $('#fieldset0').css('display', 'initial');
    $('#fieldset1').css('display', 'none');
});
