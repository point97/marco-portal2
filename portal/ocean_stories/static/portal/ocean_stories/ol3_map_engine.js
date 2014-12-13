function ol3MapEngine(selector, animate) {

  var baseLayers = {
    "Open Street Map": new ol.layer.Tile({
      source: new ol.source.OSM(),
      visible: false,
    }),
    "ESRI Ocean": new ol.layer.Tile({
      source: new ol.source.XYZ({
        url: 'http://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}'
      }),
      visible: false,
    }),
    // Google Streets
    // Google Physical
    // Google Satellite
    // Nautical Charts
  };

  var baseLayerGroup = new ol.layer.Group({
    layers: _.values(baseLayers),
  });
  var dataLayerGroup = new ol.layer.Group({
    layers: [],
  });


  var view = new ol.View();

  var map = new ol.Map({
    target: selector,
    layers: [
      baseLayerGroup,
      dataLayerGroup,
    ],
    view: view,
    interactions: [],
    controls: [],
  });
  map.on("render", function(){
    console.log(e);
  });

  var typeCreateHandlers = {
    'XYZ': function(l) {
      var fixedUrlTemplate = l.url.replace(/\$\{([xyz])\}/g, '\{$1\}')
      return new ol.layer.Tile({
        source: new ol.source.XYZ({
          url: fixedUrlTemplate,
        })
      });
    },
    'Vector': function(l) {
      return new ol.layer.Vector({
        source: new ol.source.GeoJSON({
          url: l.url,
        }),
        style: new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: l.vector_outline_color,
            width: 1.5,
          }),
          fill: new ol.style.Fill({
            color: l.vector_color,
          }),
        }),
        opacity: l.opacity,
      });
    },
    'WMS': function(l) {
      return new ol.layer.Tile({
        // extent: [-13884991, 2870341, -7455066, 6338219],
        source: new ol.source.TileWMS( ({
          url: l.url,
          params: {'LAYERS': l.arcgis_layers, 'TILED': true}
        }))
      })
    },
  }

  function wrapAnimations(animations, after) {
    return function(map, state) {
      for (i = 0; i < animations.length; ++i) {
        if (!animations[i](map, state)) {
          animations.splice(i--, 1);
        }
      }
      if (animations.length == 0) {
        after(map, state);
        return false;
      }
      return true;
    }
  }

  return {
    setView: function(center, zoom, afterFunc){
      console.info("set view center: " + center + ", zoom: " + zoom);
      // only animate if enabled and there is a previous view state
      if (animate && view.getCenter() && view.getZoom()) {
        // dataLayerGroup.setVisible(false);
        map.beforeRender(wrapAnimations([
          ol.animation.pan({
            duration: 2000,
            source: /** <at> type {ol.Coordinate} */ (view.getCenter())
          }),
          ol.animation.zoom({
            duration: 2000,
            resolution: view.getResolution(),
            source: /** <at> type {ol.Coordinate} */ (view.getZoom())
          })
          ], function() {
            afterFunc();
            dataLayerGroup.setVisible(true);
          })
        );
      } else {
        afterFunc();
      };

      view.setCenter(ol.proj.transform(center, 'EPSG:4326', 'EPSG:3857'));
      view.setZoom(zoom);
    },
    newDataLayer: function(l) {
      if (!typeCreateHandlers.hasOwnProperty(l.layer_type)) {
        console.warn("Unknown layer_type: " + l.layer_type);
        return null;
      }

      var layerObj = typeCreateHandlers[l.layer_type](l);
      layerObj.setVisible(false);
      dataLayerGroup.getLayers().push(layerObj);

      return layerObj;
    },
    showLayer: function(layer){ return layer.setVisible(true) },
    hideLayer: function(layer){ return layer.setVisible(false) },
    baseLayers: baseLayers,
    updateSize: function(){
      map.updateSize();
    }
  };
}
