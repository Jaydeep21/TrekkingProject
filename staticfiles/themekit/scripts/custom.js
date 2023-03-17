/*
 * ===========================================================
 * CUSTOM.JS 
 * ===========================================================
 * This is a custom file and it's used only on this template.
 *
*/

"use strict";
(function ($) {
    $(document).ready(function () {
        var sliders = $("section.alpins-slider");
        $(sliders).on("mouseenter", ".glide__slide:not(.glide__slide--clone)", function () {
            var slider = $(this).closest("section").find(".background-slider");
            $(slider).find(" > div").addClass("remove-active").eq($(this).index()).addClass("active").removeClass("remove-active");

            setTimeout(function () {
                $(slider).find(".remove-active").removeClass("active remove-active");
            }, 800); 
        }); 
    });
}(jQuery)); 
