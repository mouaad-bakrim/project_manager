
function updateURLParameter(url, param, paramVal)
{
    var TheAnchor = null;
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";

    if (additionalURL) 
    {
        var tmpAnchor = additionalURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor = tmpAnchor[1];
        if(TheAnchor)
            additionalURL = TheParams;

        tempArray = additionalURL.split("&");

        for (var i=0; i<tempArray.length; i++)
        {
            if(tempArray[i].split('=')[0] != param)
            {
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }        
    }
    else
    {
        var tmpAnchor = baseURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor  = tmpAnchor[1];

        if(TheParams)
            baseURL = TheParams;
    }

    if(TheAnchor)
        paramVal += "#" + TheAnchor;

    var rows_txt = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rows_txt;
}
function reset_filter(){
    $('#filterForm').trigger("reset");
    $('#filterForm').find('.select2-hidden-accessible').val(null).trigger('change');
}$(window).on('pageshow', function(){
    $('#loading').hide();
});
$(document).ready(function(){
    $(".filter-form ").on("submit", function(){
        $('#loading').show();
    });
    $(".menu-item").on("click", function(){
        if (!$(this).hasClass("menu-accordion") && !$(this).hasClass("menu-perso")){
            $('#loading').show();
        }
    });//click
    $(".detail-link").on("click", function(){
        if (!$(this).hasClass("menu-accordion") && !$(this).hasClass("menu-perso")){
            $('#loading').show();
        }
    });//click
});//document ready

$(".dateinput").flatpickr({
    dateFormat: "d/m/Y",    
    "locale": "fr"
});
$(".mae-filter-form").find('input,textarea').addClass("form-control form-control-solid");
$(".mae-filter-form").find('select').addClass("form-select");
$(".date-range-picker").flatpickr({
    dateFormat: "d/m/Y",    
    locale: "fr",
    mode: "range",

});
        
function startCountdown_loader(seconds) {
    var countdownTimer = setInterval(function() {
      // Select the loading text div
      var loadingTextDiv = document.getElementById('loading-text');
  
      // Update the div's content with the remaining seconds
      loadingTextDiv.textContent = `Traitement en cours… ${seconds}s`;
  
      // Decrease the seconds
      seconds -= 1;
  
      // If the countdown reaches 0, clear the interval to stop the countdown
      if (seconds < 0) {
        clearInterval(countdownTimer);
        // Update the div to indicate the loading is complete
        loadingTextDiv.textContent = 'Encore quelques instants…';
      }
    }, 1000); // Schedule the interval to run every 1000 milliseconds (1 second)
}

function isMenuExpanded() {
    var toggleElement = document.getElementById('kt_aside_toggle');
    return toggleElement.getAttribute('data-kt-toggle-state') === 'active';
}

$('#kt_aside_toggle').on('click', function() {
    var menuExpanded = $('#kt_aside_toggle').hasClass('active');
    $.ajax({
        url: '/save-menu-state/' + menuExpanded+'/',
        method: 'GET',
    });
});

function toggleFilterCard(){
    $("#filterCard").toggleClass('show');
    // var bsCollapse = new bootstrap.Collapse(document.getElementById('filterCard'));
    var menuExpanded = $('#filterCard').hasClass('show');
    $.ajax({
        url: '/save-filter-state/' + menuExpanded+'/',
        method: 'GET',
    });

    $('#funnel-icon-id').toggleClass('bi-funnel');
    $('#funnel-icon-id').toggleClass('bi-funnel-fill');
}


window.addEventListener("DOMContentLoaded", (e) => {
    $('select').on('select2:select', function (e) {
        $(this).closest('select').get(0).dispatchEvent(new Event('change'));
    });
});
