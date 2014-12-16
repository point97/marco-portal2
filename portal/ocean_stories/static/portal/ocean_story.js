function newOceanStory(mapElement, story, animate) {

  var map;
  var mapEngine = ol3MapEngine(mapElement[0], animate);

  function bindScrollAnimationToLinks(selector) {
    if (animate) {
      // copied with modification from
      // http://www.paulund.co.uk/smooth-scroll-to-internal-links-with-jquery
      $(document).ready(function(){
        // only animate intra-page links inside .content
        $(selector).on('click',function (e) {
          e.preventDefault();

          var target = this.hash;
          $target = $(target);

          $('html, body').stop().animate({
            'scrollTop': $target.offset().top
          }, 900, 'swing', function () {
            window.location.hash = target;
          });
        });
      });
    }
  }

  bindScrollAnimationToLinks('a[href^="#"].animate');

  function callIfChanged(f) {
    var state;
    return function(newState) {
      if (newState !== state) {
        state = newState;
        f(state);
      }
    }
  }

  bindCurtain($('.curtain'), callIfChanged(function(collapsed){
    console.info('set collapse: '+collapsed)
    mapElement.toggleClass('half', collapsed);
    mapElement.toggleClass('full', !collapsed);
    if (map) map.updateSize();
  }));

  $.getJSON("/data_manager/api/layers", function(data) {

    var dataLayers = _.indexBy(data, 'id');
    _.each(dataLayers, function(d) {
      if (d.layer_type == 'ArcRest') {
        hackyMarineCadastreLayerConversion(d);
      }
    })
    oceanStoryMap = newMap(mapEngine, story, dataLayers);

    scrollSpy('.content', 'a.anchor[id^=\'section-\']', function(sectionIndex){
      return oceanStoryMap.goToSection(sectionIndex);
    })

    setMapHeight();
    $(window).scroll(setMapHeight);
    $(window).resize(setMapHeight);
  });

}
