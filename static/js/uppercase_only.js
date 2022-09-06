jQuery_3_6_0(document).ready(function(){
    jQuery_3_6_0('.js-uppercase-only').on('input', function(){
        const p=this.selectionStart;
        this.value=this.value.toUpperCase();
        this.setSelectionRange(p, p);
    });
});