var OceanStory = (function() {

  function baseLayerSetter(engine) {
    var current;
    return function(value) {
      // noop
      if (value == current) return;

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

    function createDataLayer(l) {
      console.log("Create data layer " + l.name + ' of layer_type ' +l.layer_type);
      if (engine.typeCreateHandlers.hasOwnProperty(l.layer_type)) {
        return engine.typeCreateHandlers[l.layer_type](l);
      }
    }

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
          layerCache[id] = createDataLayer(layerCatalog[id]);
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
      s = story.sections[section];

      setBaseLayer(s.baseLayer);
      setDataLayers(s.dataLayers);
      engine.setView(s.view.center, s.view.zoom);

      activeSection = section;
    }

    goToSection(0);

    return {
      goToSection: goToSection,
    };
  }

  return {
    create: create,
  };
}());
