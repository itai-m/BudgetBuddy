$(".controlTd").click(function () {
  $(this).children(".settingsIcons").toggleClass("display");
  $(this).children(".settingsIcon").toggleClass("openIcon");
});

$('a').each(function() {
   var a = new RegExp('/' + window.location.host + '/');
   if(!a.test(this.href)) {
       $(this).click(function(event) {
           event.preventDefault();
           event.stopPropagation();
           window.open(this.href, '_blank');
       });
   }
});

$("#content a[href^='http://']").attr("target","_blank");