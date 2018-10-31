hideall = () => {
    $.each($(".tab-data"), function(k, v) {
        v.style.display = "none";
    });
}

hideallHorz = () => {
    $.each($(".tab-data-Horz"), function(k, v) {
        v.style.display = "none";
    });
}

showActive = () => {
    $.each($(".tab"), function(k, v) {
        if (v.classList.contains("active")) {
            hideall();
            tabToShow = this.getAttribute("tab");
            tab = document.getElementById(tabToShow);
            tab.style.display = "";
        }
    });
}

showHorzActive = () => {
    $.each($(".horz-tab"), function(k, v) {
        if (v.classList.contains("active")) {
            hideallHorz();
            tabToShow = this.getAttribute("tab");
            tab = document.getElementById(tabToShow);
            tab.style.display = "";
        }
    });
}

$(".tab").click(function() {
    $.each($(".tab"), function(k, v) {
        v.classList.remove("active");
    })
    $(this).addClass("active");
    showActive();
});

$(".horz-tab").click(function() {
    $.each($(".horz-tab"), function(k, v) {
        v.classList.remove("active");
    })
    $(this).addClass("active");
    showHorzActive();
});

hideall();
hideallHorz();
showActive();
showHorzActive();