var ol = require('openlayers');

module.exports = {
  "Ocean": new ol.layer.Tile({
    source: new ol.source.XYZ({
      url: 'http://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}',
      maxZoom: 17,
    }),
    visible: false,
  }),
  "Open Street Map": new ol.layer.Tile({
    source: new ol.source.OSM(),
    visible: false,
  }),
  "Streets": new ol.layer.Tile({
    source: new ol.source.XYZ({
      url: 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
      maxZoom: 17,
    }),
    visible: false,
  }),
  "Physical": new ol.layer.Tile({
    source: new ol.source.XYZ({
      url: 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
      maxZoom: 20,
    }),
    visible: false,
  }),
  "Satellite": new ol.layer.Tile({
    source: new ol.source.XYZ({
      url: 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      maxZoom: 20,
    }),
    visible: false,
  }),
  "Nautical Charts": new ol.layer.Tile({
    source: new ol.source.TileWMS({
      url: "http://egisws02.nos.noaa.gov/ArcGIS/services/RNC/NOAA_RNC/ImageServer/WMSServer",
      maxZoom: 13,
      projection: "EPSG:3857",
    }),
    visible: false,
  }),
};
