// Basic Gulp File
//
var gulp = require('gulp');
var path = require('path');
var gutil = require('gulp-util');
var less = require('gulp-less');
var sourcemaps = require('gulp-sourcemaps');
var autoprefixer = require('gulp-autoprefixer');
var concat = require('gulp-concat');
var notify = require("gulp-notify");
var bower = require('gulp-bower');
var browserSync = require('browser-sync');
var webpackConfig = require('./webpack.config');
var webpack = require('webpack');;

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
gulp.task('css', function() {
    return gulp
        .src(path.join(config.stylePath, 'marco_site.less'))
        .pipe(sourcemaps.init())
        .pipe(less())
        .pipe(autoprefixer())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(config.outDir + '/css'))
        .on("error", notify.onError(function (error) {
            return "Error: " + error.message;
        }))
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
