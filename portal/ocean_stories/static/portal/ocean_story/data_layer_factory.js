var ol = require('openlayers');

var typeHandlers = {
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

module.exports = function(l) {
  if (!typeHandlers.hasOwnProperty(l.layer_type)) {
    console.warn("Unknown layer_type: " + l.layer_type);
    return null;
  }  
  return typeHandlers[l.layer_type](l);
}
