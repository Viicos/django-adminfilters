var DepotManager = function (element) {
    var $ = django.jQuery;
    var $wrapper = django.jQuery(element);
    var $container = $wrapper.find("ul.adminfilter");
    var $select = $container.find("select");
    var $input = $container.find("input[type=text]");
    var $button = $container.find("a.button");
    var qs = $container.data("qs");

    var saveAs = function () {
        if ($input.val()) {
            var url = qs + "&" + $container.data("lk") + "=" + encodeURIComponent($input.val());
            location.href = url;
        }
    };

    $select.on("change", function (e) {
        var $option = $("#depot_manager option:selected");
        var qs = $option.data("qs");
        if (qs) {
            location.href = qs;
        }
    });
    $button.on("click", saveAs);
    $input.on("keypress", function (e) {
        if (e.which === 13) {
            saveAs();
        }
    });

};