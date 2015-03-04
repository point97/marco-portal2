var _ = require('lodash')
    curtain = require('./curtain')
    hackyMarineCadastreLayerConversion = require('./hacky_marine_cadastre_layer_conversion')
    scrollSpy = require('./scroll_spy')
    ol3MapEngine = require('./ol3_map_engine')
    oceanStoryMap = require('./map')
    polyfills = require('./polyfills');

function mount(mapElement, story, animate) {

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

  // returns a setter that calls the passed function whenever the value changes
  // this could be useful as part of a utility library
  function callIfChanged(f) {
    var state;
    return function(newState) {
      if (typeof(state) == "undefined" || newState !== state) {
        state = newState;
        f(state);
      }
    }
  }

  curtain($('.curtain'), callIfChanged(function(collapsed){
    console.info('set collapse: '+collapsed)
    mapElement.toggleClass('half', collapsed);
    mapElement.toggleClass('full', !collapsed);
    mapEngine.updateSize();
  }));

  $.getJSON("/data_manager/api/layers/", function(data) {

    var dataLayers = _.indexBy(data, 'id');
    _.each(dataLayers, function(d) {
      if (d.layer_type == 'ArcRest') {
        hackyMarineCadastreLayerConversion(d);
      }
    })
    map = oceanStoryMap(mapEngine, story, dataLayers);
    scrollSpy('.content', 'a.anchor[id^=\'section-\']', function(sectionIndex){
      return map.goToSection(sectionIndex);
    })
  });
}

module.exports = mount;
window.oceanStory = module.exports;
