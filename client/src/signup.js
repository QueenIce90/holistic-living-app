
$(document).ready(function() {
    $('#signupForm').submit(function(e) {
        e.preventDefault();
        var name = $('#name').val();
        var email = $('#email').val();
        var password = $('#password').val();
        var confirmPassword = $('#confirmPassword').val();

        if (name === '' || email === '' || password === '' || confirmPassword === '') {
            $('#errorMessage').text('Please fill in all fields.');
        } else if (password !== confirmPassword) {
            $('#errorMessage').text('Passwords do not match.');
        } else {
            alert('Sign up successful!');
            // Perform sign up logic here
        }
    });
});

export default Signup