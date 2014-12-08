function hackyMarineCadastreLayerConversion(l) {
  l.layer_type = "WMS";
  l.url = l.url.replace(
    /^(http:\/\/coast.noaa.gov\/arcgis)\/rest\/(services\/MarineCadastre\/[^/]+\/MapServer)\/export$/,
    '$1/$2/WMSServer'
  );

  var idMappings = {
    "http://coast.noaa.gov/arcgis/services/MarineCadastre/NavigationAndMarineTransportation/MapServer/WMSServer": {
      7: 2,
      8: 1,
      9: 0,
    },
    "http://coast.noaa.gov/arcgis/services/MarineCadastre/OceanEnergy/MapServer/WMSServer": {
      4: 0,
      3: 1,
    }
  }

  if (idMappings.hasOwnProperty(l.url)) {
    var mapping = idMappings[l.url];
    var arcRestLayers = l.arcgis_layers.split(',');
    mappedLayers = _.map(arcRestLayers, function(restId) {
      return mapping.hasOwnProperty(restId) ? mapping[restId] : restId
    });
    l.arcgis_layers = mappedLayers.join(',');
  }
  return l;
}
