# **Changelog**

All notable changes to the frontend asset should be documented in this file, including:

-   **Added** for new features.
-   **Changed** for changes in existing functionality.
-   **Deprecated** for soon-to-be removed features.
-   **Removed** for now removed features.
-   **Fixed** for any bug fixes.
-   **Security** in case of vulnerabilities.

## 2018-11-13

### Fixed

-   Fix css sourcemaps: update 'fast-sass' task in gulpfile.js to generate the style.min.css.map

### Changed

-   Use 'gulp-cssnano' to minify css

### Removed

-   Remove redundant npm packages: 'yargs', 'gulp-clean-css' and 'gulp-cssmin'

### Changed

-   Update gulp packages to the latest version and seperate dependencies and devDependencies

## 2018-12-11

### Added

-   Add style lint to gulpfile.js

### Changed

-   Update css files to use variables for color, padding, ...
-   Improve css files structure
-   Rename some of css files

### Fixed

-   Fix the css files format using style lint and prettier

### Removed

-   daterangepicker.scss
-   rTables.scss
-   tab.scss
-   ultraselect.scss

### Added

-   Add Eslint to gulpfile.js

### Fixed

-   Fix the main.js files format using Eslint

### Changed

-   Update Side menu and hamburger menu
-   Improve css files structure
-   Rename some of css files and js class for menu

### Changed

- Update main.js structure to follow object pattern

### Changed

- remove hover state from touch devices(except desktop) and add active state instead
