//https://github.com/webpack/webpack/issues/503
var path = require('path');

var projectRoot = path.join(__dirname,'..','..');
var projectApps = [
  'portal/ocean_stories',
].map(function(app){ return path.join(projectRoot,app,'static')});

var roots = projectApps;
roots.push(__dirname)

module.exports = {
  entry: {
    ocean_story: "portal/ocean_story/index.js",
  },
  output: {
    path: path.join(projectRoot, 'static', 'bundles'),
    filename: "[name].js",
    chunkFilename: "[id].js",
  },
  resolve: {
    root: roots,
  },
};
