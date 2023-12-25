
/*-----------------------------------------------------------------------------------*/
/*  DOCUMENT READY
/*-----------------------------------------------------------------------------------*/
$(document).ready(function(){
    'use strict';
    // OWL CAROUSEL //
    $('.owl-carousel').owlCarousel({
      navigation: false,
      pagination: false,
      navigationText: [
      "<i class='pe-7s-angle-left'></i>",
      "<i class='pe-7s-angle-right'></i>"
      ], 
      autoPlay: 8000,
      loop: true
    });

    $('.owl-carousel-paged').owlCarousel({
      navigation: false,
      pagination: false,
      autoPlay: 8000,
      loop: true
    });

    $('#single-slider').owlCarousel({
      navigation: false,
      pagination: true,
      autoPlay: 8000,
      loop: true
    });

    $('.owl-carousel-highlighted').owlCarousel({
      navigation: false,
      pagination: false,
      navigationText: [
      "<i class='pe-7s-angle-left'></i>",
      "<i class='pe-7s-angle-right'></i>"
      ], 
      autoPlay: 8000,
      loop: true,      
        afterAction: function(el){
           //remove class active
           this
           .$owlItems
           .removeClass('active')
          
           //add class active
           this
           .$owlItems //owl internal $ object containing items
           .eq(this.currentItem + 1)
           .addClass('active')
          
         }
    });

    jQuery('.countup').counterUp({
        delay: 10,
        time: 1000
    });


    /* Slide Sync to Carousel */
    $(".prev-bs-slide").on("click",function(event) {
      event.preventDefault(); 
      jQuery('#headerwrap').data('backstretch').prev();
    });
    $(".next-bs-slide").on("click",function(event) {
      event.preventDefault(); 
      jQuery('#headerwrap').data('backstretch').prev();
    });

    $(".side-menu .nav").metisMenu({
        toggle: false
    });

    // ANIMATED ONLY IF NOT AT TOP OF PAGE ON LOAD //
    var $win = $(window);
    if ($win.scrollTop() == 0)
        jQuery('.navbar-fixed-top').addClass('wow');
    else if ($win.height() + $win.scrollTop() == $(document).height()) {
         jQuery('.navbar-fixed-top').removeClass('wow');
    }

    // ADD SLIDEDOWN ANIMATION TO DROPDOWN //
    $('.header-fixed-top .dropdown').on('show.bs.dropdown', function(e){
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
    });

    // ADD SLIDEUP ANIMATION TO DROPDOWN //
    $('.header-fixed-top .dropdown').on('hide.bs.dropdown', function(e){
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
    });

    //NEAT VID EMBEDS
    $().prettyEmbed({ useFitVids: true });

    var magnificPopup = $.magnificPopup.instance;

    $('.lb-link').magnificPopup({
      preloader:true,
      type: 'image',
      removalDelay: 300,
      mainClass: 'fadeInDown',
      callbacks: {
          open: function() {
            magnificPopup.content.addClass('mobile');
          }
        }
    });

    //BACK TO TOP
    if ($('#back-to-top').length) {
      var scrollTrigger = 100, // px
          backToTop = function () {
              var scrollTop = $(window).scrollTop();
              if (scrollTop > scrollTrigger) {
                  $('#back-to-top').addClass('show');
              } else {
                  $('#back-to-top').removeClass('show');
              }
          };
      backToTop();
      $(window).on('scroll', function () {
          backToTop();
      });
      $('#back-to-top').on('click', function (e) {
          e.preventDefault();
          $('html,body').animate({
              scrollTop: 0
          }, 700);
      });
    }
    
    $('.vertical-center').flexVerticalCenter({ cssAttribute: 'padding-top' });

    //CONTACT FORM
    $('#contactform').submit(function(){
      var action = $(this).attr('action');
      $("#message").slideUp(750,function() {
      $('#message').hide();
      $('#submit').attr('disabled','disabled');
      $.post(action, {
        name: $('#name').val(),
        email: $('#email').val(),
        website: $('#website').val(),
        comments: $('#comments').val()
      },
        function(data){
          document.getElementById('message').innerHTML = data;
          $('#message').slideDown('slow');
          $('#submit').removeAttr('disabled');
          if(data.match('success') != null) $('#contactform').slideUp('slow');
          $(window).trigger('resize');
        }
      );
      });
      return false;
    });

    $(".rotate").textrotator({
      animation: "dissolve",
      separator: ",",
      speed: 2500 // How many milliseconds until the next word show.
    });

    $('.match-height').matchHeight({
        byRow: true,
        property: 'height',
        target: null,
        remove: false
    });


    $("#mapwrapper").gMap({ 
        controls: true,
        scrollwheel: false,
        markers: [{     
            latitude:40.7566,
            longitude: -73.9863,
        icon: { image: "assets/img/marker.png",
            iconsize: [44,44],
            iconanchor: [12,46],
            infowindowanchor: [12, 0] } }],
        icon: { 
            image: "assets/img/marker.png", 
            iconsize: [26, 46],
            iconanchor: [12, 46],
            infowindowanchor: [12, 0] },
        latitude:40.7566,
        longitude: -73.9863,
        zoom: 14,
        styles: [{"featureType":"all","elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#000000"},{"lightness":40}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#000000"},{"lightness":16}]},{"featureType":"all","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":17},{"weight":1.2}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":21}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":16}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":19}]},{"featureType":"water","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":17}]}]
    });

    //SIDE NAV MOBILE
    $('#side-menu-toggle').on('click', function(event){
      event.preventDefault();
      $(this).toggleClass('open');
      $('#side-menu-toggle i').toggleClass('fa-bars');
      $('#side-menu-toggle i').toggleClass('fa-times');
      $('#side-wrapper').toggle();
    });

    // ONEPAGER XTRA //
    $('body').scrollspy({
        target: '.navbar-fixed-top'
    });

    // FULLSCREEN FIX //
    var windowHeight = $(window).innerHeight();
    var isMobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    if( !isMobileDevice ) {
        $('#headerwrap.fullheight').css('height', windowHeight);
        $(window).resize(function() {
            $('#headerwrap.fullheight').css('height', windowHeight);
        });
    }

    // ANIMATE ONCE PAGE LOAD IS OVER //
    Pace.on("done", function(){
        new WOW().init();
        $(window).trigger('resize');
    });

    // SEARCH //
    $('a[href="#search"]').on('click', function(event) {
        event.preventDefault();
        $('#search-wrapper').addClass('open');
        $('#search-wrapper > form > input[type="search"]').focus();
    });
    
    $('#search-wrapper, #search-wrapper button.close').on('click keyup', function(event) {
        if (event.target == this || event.target.className == 'close' || event.keyCode == 27) {
            $(this).removeClass('open');
        }
    });
    


    // ONEPAGER //
    $('a.page-scroll').on('click', function(event){
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });

    $('.entry-content table, #post-content table').addClass('table');
    $('.entry-content dl, #post-content dl').addClass('dl-horizontal');
    //$(window).trigger('resize');
});

/*-----------------------------------------------------------------------------------*/
/*  WINDOW LOAD
/*-----------------------------------------------------------------------------------*/
$(window).load(function() {
    'use strict';

    var portfolio_selectors = $('.portfolio-filter li a');

    if(portfolio_selectors!='undefined'){
        var portfolio = $('.portfolio-items');
        portfolio.imagesLoaded( function(){
             portfolio.isotope({
                itemSelector : 'li',
                layoutMode : 'fitRows',
                transitionDuration: '0.8s'
            });
        });

        portfolio_selectors.on('click', function(e){
            e.preventDefault();
            portfolio_selectors.removeClass('active');
            $(this).addClass('active');
            var selector = $(this).attr('data-filter');
            portfolio.isotope({ filter: selector });
            return false;
        });
    }

    var boxed_portfolio_selectors = $('.boxed-portfolio-filter li a');

    if(boxed_portfolio_selectors!='undefined'){
        var boxed_portfolio = $('.boxed-portfolio-items');
        boxed_portfolio.imagesLoaded( function(){
             boxed_portfolio.isotope({
                itemSelector : 'li',
                layoutMode : 'fitRows'
            });
        });

        boxed_portfolio_selectors.on('click', function(e){
            e.preventDefault();
            boxed_portfolio_selectors.removeClass('active');
            $(this).addClass('active');
            var selector = $(this).attr('data-filter');
            boxed_portfolio.isotope({ filter: selector });
            return false;
        });
    }

    var masonry_portfolio_selectors = $('.masonry-portfolio-filter li a');
    var masonry_container = $('.masonry-portfolio');

    if(masonry_portfolio_selectors!='undefined'){
        var masonry_portfolio = $('.masonry-portfolio-items');
        masonry_portfolio.imagesLoaded( function(){
             masonry_portfolio.isotope({
                itemSelector: '.masonry-portfolio-item',
                masonry: {
                  columnWidth: masonry_container.width() / 3
                }
            });
        });

        masonry_portfolio_selectors.on('click', function(e){
            e.preventDefault();
            masonry_portfolio_selectors.removeClass('active');
            $(this).addClass('active');
            var selector = $(this).attr('data-filter');
            masonry_portfolio.isotope({ filter: selector });
            return false;
        });
    }

//  was 300
    // PRELOADING SCREEN
    jQuery('a:not([target="_blank"]):not([href*=#]):not([href^=mailto]):not(.fancybox-media):not(.btn.responsive-menu):not(a[href$="jpg"]):not([href$="jpeg"]):not(a[href$="gif"]):not(a[href$="png"]):not(a.ajax-link)').on('click', function(){
      var href = jQuery(this).attr('href');
      jQuery('.preloader').fadeIn(2);
      setTimeout(function(){
        window.location = href;
      }, 2);
      return false;
    });

    jQuery('#menu-toggle').on('click', function(e){
        $('.animated-navigation #main-navigation').toggleClass("menu-active"); //you can list several class names 
        e.preventDefault();
    });

    /* SINGLE PAGE SECIION */
    if ($(".single-page-section").length > 0){

      $('.single-page-section').each(function(){
        var sectionId = $(this).attr('id');
        $('<a href="#'+sectionId+'" class="section-link-'+sectionId+' smoothie"><i class="fa fa-circle-o"></i></a>').appendTo('#single-pager-navigation-wrapper');
        $('#'+sectionId+'').bind('inview', function(event, isInView) {
          if (isInView) {
            $('.active.theme-accent-color').removeClass('active theme-accent-color');

            $('.section-link-'+sectionId+'').addClass('active theme-accent-color');
          } else {
            $('.section-link-'+sectionId+'').removeClass('active theme-accent-color');
          }
        });
      });
      $(document).on('click', '#single-pager-navigation-wrapper a', function(){
          var $anchor = $(this);
          $('html, body').stop().animate({
              scrollTop: $($anchor.attr('href')).offset().top
          }, 1500, 'easeInOutExpo');
          event.preventDefault();
      });

      var controlHeight = $('#single-pager-navigation-wrapper').outerHeight();
      $('#single-pager-navigation-wrapper').css({
        'margin-top': '-'+controlHeight/2+'px'
      });

    }

});

// $(window).on("backstretch.after", function (e, instance, index) {
//     BackgroundCheck.init({
//         targets: '.navbar-fixed-top, #headerwrap',
//         images: '.backstretch >img'
//     })
//     BackgroundCheck.refresh();
// });

// cookies code 
const cookieBox = document.querySelector(".wrapper"),
  buttons = document.querySelectorAll(".button");

const executeCodes = () => {
  //if cookie contains codinglab it will be returned and below of this code will not run
  if (document.cookie.includes("barzoz")) return;
  cookieBox.classList.add("show");
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
        console.log("Button clicked");
      cookieBox.classList.remove("show");
      //if button has acceptBtn id
      if (button.id == "acceptBtn") {
        //set cookies for 1 month. 60 = 1 min, 60 = 1 hours, 24 = 1 day, 30 = 30 days
        document.cookie = "cookieBy= barzoz; max-age=" + 60 * 60 * 24 * 30;
      }
    });
  });
};
//executeCodes function will be called on webpage load
window.addEventListener("load", executeCodes); 