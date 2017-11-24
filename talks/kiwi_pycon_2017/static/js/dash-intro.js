$(document).ready(function(){

    $(document).keydown(function(e){
        // bind various keys...
        
        if (e.keyCode == 37) {
            // left key press navigates back
            $('#prev-page').click();
            return false;
        } else if (e.keyCode == 39) {
            // right key press navigates forwards
            $('#next-page').click();
            return false;
        }

        // TODO:
        // u for undo
        // r dor redo
        // need to find class ._dash-undo-redo
        // first child is undo, second if it exists is redo
    });

});
