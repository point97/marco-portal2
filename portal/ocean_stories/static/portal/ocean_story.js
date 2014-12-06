var OceanStory = (function() {

  function baseLayerSetter(engine) {
    var current;
    return function(value) {
      // noop
      if (value == current) return;

      console.log("set base layer: " + value)
      // return early if layer is unknown
      if (!engine.baseLayers.hasOwnProperty(value)) return;

      // add layer
      engine.addLayer(engine.baseLayers[value], true);

      // remove old layer if there is one
      if (current) engine.removeLayer(engine.baseLayers[current]);

      current = value;
    }
  }

  function dataLayersSetter(engine, layerCatalog) {
    var layerCache = {};
    var currentLayers = [];

    return function(layers) {
      var layerKeys = Object.keys(layers)

      // trim unused layers
      _.each(_.difference(currentLayers, layerKeys), function(id) {
        console.log("Remove data layer " + layerCatalog[id].name);
        if (layerCache[id]) {
          engine.removeLayer(layerCache[id]);
        }
      });

      // add new layers
      _.each(_.difference(layerKeys, currentLayers), function(id) {
        // create layer object if it hasn't been already
        if (!layerCache.hasOwnProperty(id)) {
          layerCache[id] = engine.createDataLayer(layerCatalog[id]);
        }
        console.log("Add data layer " + layerCatalog[id].name);
        if (layerCache[id]) {
          engine.addLayer(layerCache[id]);
        }
      });

      // set layer properties
      _.each(layerKeys, function(id){
        console.log("set layer props for "+layerCatalog[id].name)
      });
      currentLayers = layerKeys;
    }
  }

  function create(engine, story, layerCatalog) {
    var activeSection;
    var setBaseLayer = baseLayerSetter(engine);
    var setDataLayers = dataLayersSetter(engine, layerCatalog);

    function goToSection(section) {
      var s = story.sections[section];
      console.log("go to section "+section);

      setBaseLayer(s.baseLayer);
      setDataLayers(s.dataLayers);
      engine.setView(s.view.center, s.view.zoom);

      activeSection = section;
    }

    return {
      goToSection: goToSection,
    };
  }

  return {
    create: create,
  };
}());
