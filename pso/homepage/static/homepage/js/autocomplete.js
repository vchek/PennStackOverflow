$(function() {
    $("#searchbox").autocomplete({
        source: "/autocomplete",
        minLength: 2,
    });
});
