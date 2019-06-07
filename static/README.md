
This project uses Gulp as a task runner. Gulp automates compiling SASS files into CSS, compressing images, creating webfont, ... Gulp and Gulp plugins are installed and managed via npm, the Node.js package manager.

==========================================================
THIS PROJECT REQUIRES
==========================================================

1. node and npm (Install Nodejs if you dont have it): 
    
    curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -

    sudo apt-get install -y nodejs

    gulp-cli: sudo npm install -g gulp-cli

2. Install node dependencies: (at your template derictory where has package.json )
   
   npm install (this command will install packages that are inside both dependencies and devDependencies)
   npm install --production (this command will install packages that are inside dependencies)

==========================================================
USE GULP
==========================================================
*To run a gulp build (it compile sass to css, minify it, concatenate and minify main.js, concatenate and minify vendors js )
 
 gulp build (you only need to run this command if a new js file has been added to the vendor folder)
 gulp build --production (it will only run sass or any task that has been added to the first array after argv.production condition )

*To run a gulp build and watch:
 
 gulp

*To Generate web fonts:
 
 gulp Iconfont

*To optimise images
 
 gulp imagemin
 
 *To run gulp through npm
 
  npm run dev (it is the same as "gulp" command)
  npm run build (it is the same as "gulp build" command)
  npm run production (it is the same as "gulp build --production" command)

==========================================================
USE ICON FONT
==========================================================
1. Put the .svg files into "templates/your_template/icons"

2. Run " gulp iconfont "

3. You can find icon fonts scss in "templates/your_template/css/generic/_icon-fonts.scss"

4. How to use icon font. 
   
   1).In the pseudo element before/after:
    Eg.
    span:before
    {
        @extend %icon-butterfly;
        color:red; // Change color
        font-size:20px; // Change size
    }
  
   2).Use as the class.  
   Eg. (see butterfly logo at the footer)
   <span class="icon icon-butterfly">Website by</span>

==========================================================
USE ASSET SUBMODULE
========================================================== 
1. To use asset submodule at your joomla standard install.
    1. Pull the latest code from the Joomla standard install repo.
    2. Run "git submodule init" to initialize
    3. Run "git submodule update" to fetch data



2. To commit/push code to asset submodule
    * If you want to commit and push code to asset submodule remote repo, you need to go to templates/base/asset directory. Then perform normal git process.

==========================================================
ESLint
==========================================================
1. ESLint is an open source JavaScript linting utility originally created by Nicholas C. Zakas in June 2013. Code linting is a type of static analysis that is frequently used to find problematic patterns or code that doesn’t adhere to certain style guidelines.
No rules are enabled by default. The "extends": "eslint:recommended" property in a configuration file enables rules that report common problems. 
For more information about the ESLInt rules please refer to https://eslint.org/docs/rules/

2. eslint-plugin-prettier is a plugin that asks ESLint to run Prettier

3. eslint-config-prettier turns off all rules that are unnecessary or might conflict with Prettier
    1. There a few rules that eslint-config-prettier disables that actually can be enabled in some cases. For more information please refer to https://github.com/prettier/eslint-config-prettier#special-rules  