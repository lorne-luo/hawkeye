var argv = require("yargs").argv;
var isProduction = argv.production;

var gulp = require("gulp"),
    sass = require("gulp-sass"),
    cssnano = require("gulp-cssnano"),
    autoprefixer = require("gulp-autoprefixer"),
    sourcemaps = require("gulp-sourcemaps"),
    rename = require("gulp-rename");

// Any package that is only required on dev should be added here
if (!isProduction) {
    var eslint = require("gulp-eslint"),
        concat = require("gulp-concat-util"),
        uglify = require("gulp-uglify"),
        imagemin = require("gulp-imagemin"),
        del = require("del"),
        iconfont = require("gulp-iconfont"),
        iconfontCss = require("gulp-iconfont-css"),
        gulpStylelint = require("gulp-stylelint"),
        prettier = require("gulp-plugin-prettier"),
        cache = require("gulp-cached");
}

/**
 * Variables
 */
fontName = "Icons";

var paths = {
    imageSrcFiles: "../../img/**/*",
    imagesDestFolder: "../../img",
    sassSrcFiles: "css/**/*.scss",
    styleLintSrcFiles: function () {
        return [
            this.sassSrcFiles,
            "!css/iconfonts_template/*.scss",
            "!css/vendors/*"
        ];
    },
    sassDestFolder: "css",
    jsSrcFiles: "js/main.js",
    jsDestFolder: "js",
    vendorSrcFolder: "js/vendor/*.js",
    vendorDestFolder: "js/vendor",
    vendorDestFile: "js/vendor/vendor.min.js",
    watchCssFiles: "css/**/*.{scss,sass}",
    watchJsFiles: "js/**/*.js",
    iconfontSrcFiles: "icons/*.svg",
    iconfontDestFolder: "fonts/icon-fonts",
    iconfontScssDestFile: "../../css/generic/_icon-fonts.scss",
    iconfontTemplateFile: "css/iconfonts_template/_icons.scss",
    iconfontFontsDestFolder: "../fonts/icon-fonts/"
};

/**
 * Image optimization
 */
gulp.task("imagemin", function () {
    gulp.src(paths.imageSrcFiles)
        .pipe(imagemin())
        .pipe(gulp.dest(paths.imagesDestFolder));
});

/**
 * Compile with Libass
 */
gulp.task("sass", !isProduction ? ["style-lint"] : null, function () {
    return gulp
        .src(paths.sassSrcFiles)
        .pipe(sourcemaps.init())
        .pipe(sass({ style: "expanded" }))
        .on("error", sass.logError)
        .pipe(
            autoprefixer({
                browsers: ["last 4 versions", "ie >= 11"],
                cascade: false
            })
        )
        .pipe(cssnano())
        .pipe(gulp.dest(paths.sassDestFolder))
        .pipe(rename({ suffix: ".min" }))
        .pipe(sourcemaps.write("."))
        .pipe(gulp.dest(paths.sassDestFolder));
});

/**
 * Lint and prettier to scss file
 */
gulp.task("style-lint", function () {
    return (
        gulp
            .src(paths.styleLintSrcFiles())
            // Use cache so run a task ONLY on modified file with gulp watch
            .pipe(cache("formatting"))
            .pipe(prettier.format())
            .pipe(
                gulpStylelint({
                    failAfterError: false,
                    reporters: [{ formatter: "string", console: true }],
                    // Stylelint will try to fix as many issues as possible
                    fix: true
                })
            )
            // Replace unformatted with formatted
            .pipe(
                gulp.dest(function (file) {
                    return file.base;
                })
            )
    );
});

/**
 * Concatenates js files
 */
gulp.task("scripts", !isProduction ? ["js-lint"] : null, function () {
    return gulp
        .src(paths.jsSrcFiles)
        .pipe(concat("main.js"))
        .pipe(concat.header("// file: <%= file.path %>\n"))
        .pipe(concat.footer("\n// end\n"))
        .pipe(uglify())
        .pipe(rename({ suffix: ".min" }))
        .pipe(gulp.dest(paths.jsDestFolder))
});

/**
 * Lint javascript file
 */
gulp.task("js-lint", function () {
    return gulp
        .src(paths.jsSrcFiles)
        .pipe(prettier.format())
        .pipe(eslint({
            // ESLint will try to fix as many issues as possible
            fix: true
        }))
        .pipe(eslint.format())
        .pipe(eslint.failAfterError())
        // Replace unformatted with formatted
        .pipe(
            gulp.dest(function (file) {
                return file.base;
            })
        )
});

gulp.task("clean", [], function () {
    return del(paths.vendorDestFile);
});
/**
 * Concatenates vendors js files
 */
gulp.task("vendors", ["clean"], function () {
    return gulp
        .src(paths.vendorSrcFolder)
        .pipe(concat("vendor.js"))
        .pipe(uglify())
        .pipe(rename({ suffix: ".min" }))
        .pipe(gulp.dest(paths.vendorDestFolder));
});

/**
 * Create icon fonts from several SVG icons
 */
gulp.task("iconfont", function () {
    // Put your svg here
    return gulp
        .src([paths.iconfontSrcFiles])
        // Generate iconfont scss here
        .pipe(
            iconfontCss({
                fontName: fontName,
                // Generate iconfonts scss using icons.scss
                path: paths.iconfontTemplateFile,
                // Destination scss file
                targetPath: paths.iconfontScssDestFile,
                fontPath: paths.iconfontFontsDestFolder,
                cssClass: "icon"
            })
        )
        // Generate icon font
        .pipe(
            iconfont({
                fontName: fontName,
                appendCodepoints: true,
                formats: ["ttf", "eot", "woff", "woff2", "svg"],
                normalize: true,
                fontHeight: 1001
            })
        )
        .on("codepoints", function (codepoints, options) {
            // CSS templating, e.g.
            console.log(codepoints, options);
        })
        .pipe(gulp.dest(paths.iconfontDestFolder))
});

/**
 * Build
 * gulp build --production will only run sass
 */
gulp.task(
    "build",
    !!isProduction ? ["sass"] : ["sass", "scripts", "clean", "vendors"]
);

/**
 * Default task
 */
gulp.task("default", ["sass", "scripts"], function () {
    gulp.watch(paths.watchCssFiles, ["sass"]);
    gulp.watch(paths.watchJsFiles, ["scripts"]);
});
