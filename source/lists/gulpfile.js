
// dependencies

var gulp        = require( 'gulp' );
var jshint      = require( 'gulp-jshint' );
var plumber     = require( 'gulp-plumber' );        // keep going after run-through
var rename      = require( 'gulp-rename' );
var sass        = require( 'gulp-sass' );
var uglify      = require( 'gulp-uglify' );


// establish paths

var paths = {
    js      : 'src/js/*.js' ,
    sass    : 'src/sass/*.sass'
};


// functions

gulp.task( 'sass' , function()
{
    return gulp
        .src( 'src/sass/**/*.sass' )
        .pipe( sass({ outputStyle: 'compressed' }).on( 'error' , sass.logError ) )
        .pipe( rename({ suffix : '.min' }) )
        .pipe( gulp.dest( 'static/css/' ) )
});

gulp.task( 'js' , function()
{
    return gulp
        .src( 'src/js/**/*.js' )
        .pipe( plumber() )
        .pipe( uglify() ) 
        .pipe( jshint() ) 
        .pipe( rename({ suffix : '.min' }) )
        .pipe( gulp.dest( 'static/js/' ) )
});


// defaults

gulp.task( 'watch' , function()
{
    gulp.watch( 'src/sass/**/*.sass' , [ 'sass' ] );
    gulp.watch( 'src/js/**/*.js' , [ 'js' ] );
});

gulp.task( 'default' , [
    'sass' ,
    'js' ,
    'watch'
]);

