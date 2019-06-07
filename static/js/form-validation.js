/**
 * Created by min.dang on 3/22/2017.
 */
(function ($) {
    /* Form element focus event */
    $(document).on('focus', 'input,textarea', function (e) {
        var focused_ele = $(e.target);
        var has_error = focused_ele.hasClass('rsform-error');
        var erro_box = focused_ele.next().find('span');
        /*Focus in */
        if (has_error) { // When focus in a field with validation error, the error must immediately disappear
            erro_box.addClass('formNoError');
            erro_box.removeClass('formError');
            focused_ele.removeClass('rsform-error');
        }
        $(this).on('keypress', function (e) {
            var val = focused_ele.val();
        });

        /* Focus out */
        focused_ele.focusout(function () {
            var is_valid = validate(focused_ele);
            if (!is_valid) { // When focus out a field with validation error, the error must immediately appear
                erro_box.addClass('formError');
                erro_box.removeClass('formNoError');
                focused_ele.addClass('rsform-error');
            }
            else {
                erro_box.removeClass('formError');
                erro_box.addClass('formNoError');
                focused_ele.removeClass('rsform-error');
            }
        });
    });
    
    /**
     * Validate the input field
     * @param {object} ele - input field which is on focus
     * @return {bool} is_valid - if the input field has valid value
     */
    function validate(ele) {
        var is_valid = false;
        if (ele.attr('id') == "email") {
            is_valid = validateEmail(ele.val());
        }
        else {
            is_valid = ( ele.val().length != 0 );
        }
        return is_valid;
    }
    
    /**
     * Validate email
     * @param {string} inputText - input string in email input field
     * @return {bool} is_email_valid - if the value in email input field is valid email address
     */
    function validateEmail(inputText) {
        var is_email_valid = false;
        var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (inputText.match(mailformat)) {
            is_email_valid = true;
        }
        return is_email_valid;
    }
})(jQuery);
