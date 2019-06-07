/* ========================================================================
 * shadow-scroller.js v0.0.1
 * Author: Heesien Ooi <heesien.ooi@butterfly.com.au>
 * ======================================================================== */

/**
 * Example of usage:
 * 
 * $('table').shadowScroller();
 *
 * Then add styles to your css.
 * 
 * .shadow-scroller {
 *   position: relative;
 * }
 * 
 * .shadow-scroller__scroll-view {
 *   overflow: auto;
 * }
 * 
 * .shadow-scroller__shadow-top,
 * .shadow-scroller__shadow-right,
 * .shadow-scroller__shadow-bottom,
 * .shadow-scroller__shadow-left {
 *   position: absolute;
 *   pointer-events: none;
 *   opacity: 0;
 * }
 * 
 * .shadow-scroller__shadow-right {
 *   top: 0;
 *   right: 0;
 *   width: 17px;
 *   height: 100%;
 *   background: linear-gradient(to right, rgba(3,37,58,0.01) 0%,rgba(3,37,58,0.38) 100%);
 *   transition: all 0.5s ease-in-out;
 * }
 * 
 * .shadow-scroller__shadow-left {
 *   top: 0;
 *   left: 0;
 *   width: 17px;
 *   height: 100%;
 *   background: linear-gradient(to left, rgba(3,37,58,0.01) 0%,rgba(3,37,58,0.38) 100%);
 *   transition: all 0.5s ease-in-out;
 * }
 */

(function ($) {

  "use strict";

  /**
   * Instance/ID counter
   */
  var id = 0;

  /**
   * ShadowScroller instances
   */
  var instances = [];

  /*
  |--------------------------------------------------------------------------
  | SHADOWSCROLL CLASS DEFINATION
  |--------------------------------------------------------------------------
  */

  /**
   * The constructor of our ShadowScroller class.
   * @param {HTMLElement} content Target HTML element for your plugin
   */
  function ShadowScroller(content) {
    this.id = id++;
    this.element = this.createElement(content);
    this.scrollElement = this.element.children('.shadow-scroller__scroll-view');

    // Manage the initial visibility of the shadow layers
    this.toggleShadows();

    // Register scroll event. Doesn't matter if there is no scroll on scrollview
    // because scroll event wouldn't trigger when no scroll.
    this.scrollElement.on('scroll', this.toggleShadows.bind(this));

    // Register this instance into our class variable so that later on it can be
    // used on window.resize event
    instances.push(this);
  }

  ShadowScroller.prototype = {

    /**
     * Create DOM elements needed for this plugin and wrap the content into
     * this element
     * @param  {HTMLElement} content
     * @return {jQuery}
     */
    createElement: function (content) {
      // Return when element has already created
      if (this.element) return;
      var element = null;
      var elementHTML
      = '<div class="shadow-scroller" data-shadow-scroller="' + this.id + '">'
      +   '<div class="shadow-scroller__scroll-view"/>'
      +   '<div class="shadow-scroller__shadow-top"/>'
      +   '<div class="shadow-scroller__shadow-right"/>'
      +   '<div class="shadow-scroller__shadow-bottom"/>'
      +   '<div class="shadow-scroller__shadow-left"/>'
      + '</div>';
      // Wrap content with our elements
      $(content).wrap(elementHTML);
      element = $('[data-shadow-scroller="' + this.id + '"]');
      return element;
    },

    /**
     * Check for scrollbar visibility
     * @return {Boolean} true or flase
     */
    hasScroll: function () {
      var scrollElement = this.scrollElement[0];
      if (scrollElement.scrollWidth > scrollElement.clientWidth) return true;
      if (scrollElement.scrollHeight > scrollElement.clientHeight) return true;
      return false;
    },

    /**
     * Get scroll position from all direction top/right/bottom/right
     * @return {object}
     */
    getScrollPosition: function () {
      var scrollElement = this.scrollElement[0];
      var scrollTop = scrollElement.scrollTop;
      var scrollRight = scrollElement.scrollWidth - scrollElement.scrollLeft - scrollElement.clientWidth;
      var scrollBottom = scrollElement.scrollHeight - scrollElement.scrollTop - scrollElement.clientHeight;
      var scrollLeft = scrollElement.scrollLeft;

      return {
        top: scrollTop,
        right: scrollRight,
        bottom: scrollBottom,
        left: scrollLeft
      }
    },

    /**
     * Mange all shadows visibility. Only show shadow when we can scroll into
     * that direction. In other words, only show shadows when there is scrollbar
     */
    toggleShadows: function () {
      var margin = 5;
      var scrollPos = this.getScrollPosition();
      for (var direction in scrollPos) {
        // Set opacity to 0 when scroll reached end. Optimistically, we should
        // detect scrollPos[direction] > 0. But in this case, we added a few 
        // margin to make it works more consistent.
        var opacity = scrollPos[direction] > margin ? 1 : 0;
        this.setShadowOpacity(direction, opacity);
      }
    },

    /**
     * Show/hide the select shadow layer
     * @param  {string} direction  top/right/bottom/left
     * @param  {int}    opacity value for css opacity 1 or 0
     */
    setShadowOpacity: function (direction, opacity) {
      var selectedShadow = this.element.children('[class=shadow-scroller__shadow-' + direction + ']');
      selectedShadow.css('opacity', opacity);
    }
  }

  // Register window resize event
  // This checks all ShadowScroller instances and make sure they show or hide
  // depending on their scrollbar visibility
  $(window).on('resize', function () {
    for (var i = 0; i < instances.length; i++) {
      var shadowScroller = instances[i];
      shadowScroller.toggleShadows();
    }
  });

  /*
  |--------------------------------------------------------------------------
  | SHADOWSCROLL JQUERY PLUGIN
  |--------------------------------------------------------------------------
  */

  // Register this as jquery plugin. Using $('table').shadowScroller() will
  // then initialze our ShadowScroller
  $.fn.shadowScroller = function () {
    return this.each(function () {
      new ShadowScroller(this);
    });
  }

})(jQuery);
