$(function() {
    $('#signin-form-cont input#email').first().focus();
    $('#view-terms').avgrund({			
        width: 640, // max is 640px
        height: 980, // max is 350px
        showClose: true, // switch to 'true' for enabling close button 
        showCloseText: 'Close', // type your text for close button
        closeByEscape: true, // enables closing popup by 'Esc'..
        closeByDocument: true, // ..and by clicking document itself
        holderClass: '', // lets you name custom class for popin holder..
        overlayClass: '', // ..and overlay block
        enableStackAnimation: false, // another animation type
        onBlurContainer: '', // enables blur filter for specified block 
        template: $('#terms').html()
    });
});
