jQuery_3_6_0(document).ready(function () {
    const $jsImagePopUp = jQuery_3_6_0(".js-image-pop-up");
    const $jsImagePreview = jQuery_3_6_0("#js-image-preview");

    $jsImagePopUp.click(function(){
        $jsImagePreview.attr("src", jQuery_3_6_0(this).find("img").attr("src"));
    });
});
