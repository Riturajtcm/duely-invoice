

$(document).ready(function(e) {
    $('.tab-button').click(function(){
  $('.tab-button').removeClass('on');
  $('.tab-caption').slideUp('normal');
  if($(this).next().is(':hidden')==true){
  $(this).addClass('on');
  
  $(this).next().slideDown('normal'); 
  
  
    }
  });
  $('.tab-caption').hide();
  $('.tab-caption:first').show();
  $('.tab-button:first').addClass('on');
  
});
$(document).ready(function(e) {
    $('.awardsbg').hover(function(){
  $(this).find('.figcaption').fadeIn('slow');
    },function(){
      $(this).find('.figcaption').fadeOut('slow');
      }
    
    );
    
  
});


 $(document).ready(function() {
        var owl = $('.owl-carousel3');
        owl.owlCarousel({
          loop: true,
          nav: true,
          margin: 20,
          autoplay: true,
          autoplayTimeout: 4000,
          autoplayHoverPause: true,

          responsive: {
            0: {
              items: 1
            },
            600: {
              items: 3
            },
            960: {
              items: 1
            },
            1200: {
              items: 1
            }
          }
        });
        // owl.on('mousewheel', '.owl-stage', function(e) {
        //   if (e.deltaY > 0) {
        //     owl.trigger('next.owl');
        //   } else {
        //     owl.trigger('prev.owl');
        //   }
        //   e.preventDefault();
        // });
      })
 $(document).ready(function() {
        var owl = $('.owl-carousel2');
        owl.owlCarousel({
          loop: true,
          nav: true,
          margin: 20,
          autoplay: true,
          autoplayTimeout: 4000,
          autoplayHoverPause: true,

          responsive: {
            0: {
              items: 1
            },
            600: {
              items: 1
            },
            960: {
              items: 1
            },
            1200: {
              items: 1
            }
          }
        });
        // owl.on('mousewheel', '.owl-stage', function(e) {
        //   if (e.deltaY > 0) {
        //     owl.trigger('next.owl');
        //   } else {
        //     owl.trigger('prev.owl');
        //   }
        //   e.preventDefault();
        // });
      })
 
$(document).ready(function() {
        var owl = $('.owl-carousel5');
        owl.owlCarousel({
          loop: true,
          nav: true,
          margin: 20,
          autoplay: true,
          autoplayTimeout: 4000,
          autoplayHoverPause: true,

          responsive: {
            0: {
              items: 2
            },
            600: {
              items: 3
            },
            960: {
              items: 5
            },
            1200: {
              items: 7
            }
          }
        });
        owl.on('mousewheel', '.owl-stage', function(e) {
          if (e.deltaY > 0) {
            owl.trigger('next.owl');
          } else {
            owl.trigger('prev.owl');
          }
          e.preventDefault();
        });
      })
      $(document).ready(function() {
        /*
         *  Simple image gallery. Uses default settings
         */

        $('.fancybox').fancybox();

        /*
         *  Different effects
         */




      });