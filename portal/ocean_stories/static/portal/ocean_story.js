function newOceanStory(story) {
  function newMap (engine, story, layerCatalog) {

    function normalizeSection(data) {
      data.view = {
        center: _.map(data.view.center, parseFloat),
        zoom: parseInt(data.view.zoom),
      };
    }
    story.sections.forEach(normalizeSection);

    var dataLayers = {};
    var visibleDataLayers = [];
    var currentBaseLayer;

    function defaultBaseLayer() {
      // return first base layer
      for (k in engine.baseLayers) {
        return k;
      }
    }

    function setBaseLayer(layer) {
      // return early if layer is unknown
      if (!engine.baseLayers.hasOwnProperty(layer)) {
        console.warn('attempt to set unknown base layer ' + layer);
        layer = currentBaseLayer || defaultBaseLayer();
      }

      if (layer == currentBaseLayer) return;

      console.debug('set base layer ' + layer);
      engine.showLayer(engine.baseLayers[layer], true);

      if (currentBaseLayer) {
        engine.hideLayer(engine.baseLayers[currentBaseLayer]);
      }

      currentBaseLayer = layer;

    }

    function fetchDataLayer(id) {
      if (!dataLayers.hasOwnProperty(id)) {
        if (!layerCatalog.hasOwnProperty(id)) {
          console.warn("Ignoring unknown layer id " + id);
          return false;
        }
        dataLayers[id] = engine.newDataLayer(layerCatalog[id]);
      }
      return dataLayers[id];
    }

    function setDataLayers(layers) {
      var layerKeys = Object.keys(layers)

      // trim unused layers
      _.each(_.difference(visibleDataLayers, layerKeys), function(id) {
        l = fetchDataLayer(id);
        if (l){
          engine.hideLayer(l);
        }
      });

      // add new layers
      _.each(_.difference(layerKeys, visibleDataLayers), function(id) {
        l = fetchDataLayer(id);
        if (l){
          engine.showLayer(l);
        }
      });
      visibleDataLayers = layerKeys;
    }

    return {
      goToSection: function(section) {
        if (section > story.sections.length - 1) {
          console.warn("Requested story section " + (section+1) + ", but only " + story.sections.length + " are present.")
          return;
        }
        var s = story.sections[section];

        engine.setView(s.view.center, s.view.zoom, function(){
          setBaseLayer(s.baseLayer);
          setDataLayers(s.dataLayers);
        });
      },
    };
  }

  var map = $('#map');

  var calcMapHeight = function(){
    var scrollTop = $(this).scrollTop();
    var viewHeight = $( this ).height();
    var startHeight = viewHeight - 60;
    var endHeight = viewHeight/2;
    var proportion = scrollTop/(startHeight - endHeight);
    if (proportion <= 0) {
      return startHeight;
    }
    if (proportion <= 1) {
      return endHeight*proportion + startHeight*(1-proportion);
    }
    return endHeight;
  };

  var setMapHeight = function() {
    var height = calcMapHeight();
    map.height(height);
    mapEngine.updateSize();
  };


  var oceanStoryMap;
  var mapEngine = ol3MapEngine('map');

  $.getJSON("/data_manager/api/layers", function(data) {

    var dataLayers = _.indexBy(data, 'id');
    _.each(dataLayers, function(d) {
      if (d.layer_type == 'ArcRest') {
        hackyMarineCadastreLayerConversion(d);
      }
    })
    oceanStoryMap = newMap(mapEngine, story, dataLayers);

    scrollSpy('.content', '> .section', function(sectionIndex){
      return oceanStoryMap.goToSection(sectionIndex);
    })

    setMapHeight();
    $(window).scroll(setMapHeight);
    $(window).resize(setMapHeight);
  });

}
