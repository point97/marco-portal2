// Basic Gulp File
//
var gulp = require('gulp')
    path = require('path')
    gutil = require('gulp-util')
    less = require('gulp-less')
    autoprefix = require('gulp-autoprefixer')
    notify = require("gulp-notify")
    bower = require('gulp-bower')
    browserSync = require('browser-sync')
    webpackConfig = require('./webpack.config')
    webpack = require('webpack');

var config = {
    stylePath: './styles',
    outDir: '../static'
}

config.bowerDir = config.outDir + '/bower_components';

gulp.task('bower', function() {
    return bower()
        .pipe(gulp.dest(config.bowerDir))
});

gulp.task("webpack", function(callback) {
  webpack(webpackConfig).run(function(err, stats) {
    if(err) throw new gutil.PluginError("webpack", err);
    gutil.log("[webpack]", stats.toString({
      // output options
    }));
    callback();
  });
});

gulp.task("webpack-watch", function(callback) {
  webpack(webpackConfig).watch(200, function(err, stats) {
    if(err) throw new gutil.PluginError("webpack", err);
    gutil.log("[webpack]", stats.toString({
      // output options
    }));
  });
  callback();
});

// Compiles LESS > CSS
gulp.task('css', function(){
  return gulp.src(path.join(config.stylePath, 'marco_site.less'))
  .pipe(less())
  .on("error", notify.onError(function (error) {
    return "Error: " + error.message;
  }))
  .pipe(autoprefix('last 2 version'))
  .pipe(gulp.dest(config.outDir + '/css'));
});

gulp.task('browser-sync', function(cb) {
  browserSync({
    proxy: "localhost:8111",
    open: false,
    // tunnel: true,
    
    // ghostMode: true,
    files: "../static/**/*",
  }, cb);
});

// Rerun the task when a file changes
gulp.task('watch', ['browser-sync', 'webpack-watch'], function() {
    gulp.watch(config.stylePath + '/**/*.less', ['css']);
});

gulp.task('default', ['bower', 'webpack', 'css']);
