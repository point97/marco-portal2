// Basic Gulp File
//
var gulp = require('gulp'),
    // sass = require('gulp-sass')
    sass = require('gulp-ruby-sass')
    autoprefix = require('gulp-autoprefixer')
    notify = require("gulp-notify")
    bower = require('gulp-bower');
    var browserSync = require('browser-sync');

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

gulp.task('copyjs', function() {
    // return gulp.src(config.bowerDir + '/bootstrap-sass-official/assets/javascripts/bootstrap.js')
    //     .pipe(gulp.dest(config.outDir + '/js'));
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

// Rerun the task when a file changes
gulp.task('watch', function() {
    gulp.watch(config.sassPath + '/**/*.scss', ['css']);
});

gulp.task('default', ['bower', 'icons', 'copyjs', 'css']);
