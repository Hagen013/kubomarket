// Галп используется ТОЛЬКО для разработки и сборки css, шрифтов, картинок
// Файл разделён на 3 части: common, dev, prod

var gulp = require('gulp'),
postcss = require('gulp-postcss'),
autoprefixer = require('gulp-autoprefixer'),
sass = require('gulp-sass'),
bulkSass = require('gulp-sass-bulk-import'),
sourcemaps = require('gulp-sourcemaps'),
browserSync = require('browser-sync').create(),
exec = require('child_process').exec,
fontgen = require('gulp-fontgen'),
reload = browserSync.reload;

// COMMON ====================================================================
// callback на ошибку
function onError(err) {
	exec('afplay ./error_2.mp3');
	console.log(err);
	this.emit("end");
}

// утилита для указания путей
var paths = {
	app:  './',
	css:  './static/css',
	sass: './src/sass',
	templates: './templates'
}

// генерация шрифтов - жёстко связано со сборкой scss
gulp.task('fontgen', function() {
return gulp.src("./src/fonts/**/*.{ttf,otf}")
	.pipe(fontgen({
		css_fontpath: "/static/fonts/",
		dest: "./src/fonts_build/",
		collate: true
	}));
});

// DEV =======================================================================
// css (sass)
gulp.task('styles', function() {
	console.log(paths.sass);
	gulp.src(paths.sass + '/styles.scss')
	.pipe(sourcemaps.init())
	.pipe(bulkSass())
	.pipe(sass().on('error', onError))
	.pipe(autoprefixer({browsers: ['last 2 version']}))
	.pipe(sourcemaps.write())
	.pipe(gulp.dest(paths.css));
});


// run django for browsersync
gulp.task('runserver', function() {
	exec('HOST_PORT=3000 python ../backend/manage.py runserver', function (err, stdout, stderr) {
		console.log(stdout);
		console.log(stderr);
	});
})

// browsersync
gulp.task('browserSyncTask', ['runserver'], function() {
	browserSync.init({
		notify: false,
		proxy: 'localhost:8000'
	});
});

// watch
gulp.task('watchTask', function() {
	gulp.watch(paths.sass + '/**/*.scss', ['styles', reload]);
	gulp.watch(paths.sass + '/**/**/*.scss', ['styles', reload]);
	gulp.watch([paths.templates + '/*.html',
				paths.templates + '/**/*.html',
				paths.templates + '/**/**/*.html'], reload);	
});

// default
gulp.task('default', ['styles', 'watchTask', 'browserSyncTask']);


// ==	2. TASKS production	====================================================

// IMG TO STATIC
gulp.task('prod_img', function(){
return gulp.src('./src/img/**/*.{jpg,jpeg,png,svg}')
	.pipe(gulp.dest('./static/img/'))
});

// FONT TO STATIC (AFTER FONTGEN)
gulp.task('prod_font', function() {
	return gulp.src('./src/fonts_build/**/*')
	.pipe(gulp.dest('./static/fonts/'))
});


//CSS
gulp.task('prod_css', function() {
	gulp.src(paths.sass + '/styles.scss')
		.pipe(bulkSass())
		.pipe(sass({outputStyle: 'compressed'}).on('error', onError))
		.pipe(autoprefixer({browsers: ['last 2 version']}))
		.pipe(gulp.dest(paths.css));
	gulp.src('./src/css/jquery.fancybox.min.css')
        .pipe(gulp.dest(paths.css));
});


// PRODUCTION
gulp.task('build', ['prod_css', 'prod_img', 'prod_font']);