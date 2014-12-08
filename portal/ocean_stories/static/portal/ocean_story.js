function OceanStoryMap (engine, story, layerCatalog) {

  var dataLayers = {};
  var visibleDataLayers = [];
  var currentBaseLayer;
  var activeSection;

  function setBaseLayer(layer) {
    // return early if layer is unknown
    if (!engine.baseLayers.hasOwnProperty(layer)) {
      console.warn('attempt to set unknown base layer ' + layer);
      return;
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
        engine.hideLayer(fetchDataLayer(id));
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
      var s = story.sections[section];

      engine.setView(s.view.center, s.view.zoom, function(){
        setBaseLayer(s.baseLayer);
        setDataLayers(s.dataLayers);
      });

      activeSection = section;
    },
  };
}
