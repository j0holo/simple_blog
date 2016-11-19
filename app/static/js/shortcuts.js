/*
 * Create a hotkey to insert four spaces into the texterea when
 * writing or updating a post.
 */
function insert_four_spaces(e) {
    var amount_of_spaces = 4;
    if (e.ctrlKey && (e.keyCode == 32)) {
        e.preventDefault();
        var textarea = document.getElementById("textarea");
        var spaces = " ".repeat(amount_of_spaces);
        var cursorPos = textarea.selectionStart;
        var textBeforeCursor = textarea.value.substring(0, cursorPos);
        var textAfterCursor = textarea.value.substring(
            textarea.selectionEnd,
            textarea.value.length
        );
        textarea.value = textBeforeCursor + spaces + textAfterCursor;
        cursorPos = cursorPos + spaces.length;
        textarea.selectionStart = cursorPos;
        textarea.selectionEnd = cursorPos;
        textarea.focus();
    }
}

if (document.getElementById("textarea")) {
    document.addEventListener('keyup', insert_four_spaces, false);
}
