// Basic Gulp File
//
var gulp = require('gulp')
    gutil = require ('gulp-util')
    sass = require('gulp-ruby-sass')
    autoprefix = require('gulp-autoprefixer')
    notify = require("gulp-notify")
    bower = require('gulp-bower')
    browserSync = require('browser-sync')
    webpackConfig = require('./webpack.config')
    webpack = require('webpack')(webpackConfig);

var config = {
    sassPath: './scss',
    outDir: '../static'
}

config.bowerDir = config.outDir + '/bower_components';

gulp.task('bower', function() {
    return bower()
        .pipe(gulp.dest(config.bowerDir))
});

gulp.task('icons', function() {
    return gulp.src(config.bowerDir + '/bootstrap-sass-official/assets/fonts/bootstrap/*')
        .pipe(gulp.dest(config.outDir + '/fonts/bootstrap'));
});

gulp.task("webpack", function(callback) {
  webpack.run(function(err, stats) {
    if(err) throw new gutil.PluginError("webpack", err);
    gutil.log("[webpack]", stats.toString({
      // output options
    }));
    callback();
  });
});

gulp.task("webpack-watch", function(callback) {
  webpack.watch(200, function(err, stats) {
    if(err) throw new gutil.PluginError("webpack", err);
    gutil.log("[webpack]", stats.toString({
      // output options
    }));
  });
  callback();
});


gulp.task('css', function() {
    return gulp.src(config.sassPath + '/*.scss')
        .pipe(sass({
            style: 'compressed',
            precision: 10,
            loadPath: [
                config.bowerDir + '/bootstrap-sass-official/assets/stylesheets/',
            ]
        })
            .on("error", notify.onError(function (error) {
                return "Error: " + error.message;
            })))
        .pipe(autoprefix('last 2 version'))
        .pipe(gulp.dest(config.outDir + '/css'));
});

gulp.task('browser-sync', function(cb) {
  browserSync({
    proxy: "localhost:8111",
    open: true,
    files: ["../static/css/*.css","../../static/bundles/*.js"],
  }, cb);
});

// Rerun the task when a file changes
gulp.task('watch', ['webpack-watch', 'browser-sync'], function() {
    gulp.watch(config.sassPath + '/**/*.scss', ['css']);
});

gulp.task('default', ['bower', 'icons', 'webpack', 'css']);
