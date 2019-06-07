/**
 * accordion-menu.js v1.1
 *
 * Made by Hee Sien Ooi <heesien.ooi@butterfly.com.au>
 * Insipred by Draco Chan accordionMenu.1.3.js
 *
 * Features:
 * - Accordion behaviour (only one active at time)
 * - Normal slider (allow multiple actives)
 * - Auto scroll focus
 *
 * Example of usage:
 *
 * $('#mobile-menu').accordionMenu();
 *
 * Overwrite default settings
 * $('#mobile-menu').accordionMenu({
 *   addIndicator: true,
 *   onlyOneShown: false
 * });
 */

(function($) {
  "use strict";
 
  function AccordionMenu(element, options) {
    this.$element = $(element);
    this.options = options;
    this.initialize();
    this.bindEvents();
  }

  AccordionMenu.DEFAULTS = {
    addIndicator: true, // Add indicator element into item
    activeClass: "active", // default 'open' class is based of this
    excludeActiveClass: "", // Exclude default 'open' class on this
    onlyOneShown: true, // Only alllow one open between their siblings
    autoScroll: false // Auto-scrolling when menu opened
  };

  AccordionMenu.prototype = {
    initialize: function() {
      var that = this;
      var items = this.$element.find(".deeper > a, .deeper > span");

      items.each(function() {
        var item = $(this);
        var parent = item.parent();

        // Fix onclick attribute and event binding conflict

        if (typeof this.onclick === "function") {
          item.data("onclick", this.onclick);
          this.onclick = null; // Stop onclick function from running twice
        }

        // 'data-action' is used for determine which action to triggle when element on clicked

        if (that.options.addIndicator) {
          item.attr("data-action", "link");
          item.after(
            '<i data-action="toggle" class="icon-indicator" tabindex="0"></i>'
          );
        } else {
          item.attr("data-action", "toggle");
          item.wrapInner('<span data-action="link" class="text-wrapper">');
        }

        // Add 'open' class to item for toggle to run properly

        if (
          parent.hasClass(that.options.activeClass) &&
          !parent.hasClass(that.options.excludeActiveClass)
        ) {
          item.addClass("opened");
          item.next().addClass("open");
        }
      });
    },

    bindEvents: function() {
      var that = this;
      this.$element.on(
        "keypress click",
        ".deeper > .icon-indicator, .deeper > span",
        function(e) {
          if (13 === e.which || "click" === e.type) {
            var target = $(e.target);
            e.preventDefault();

            // Call method based of target data-action
            // e.g. data-action="link" => that['link']() => that.link()

            that[target.data("action")]($(this));
          }
        }
      );
    },

    link: function($item) {
      // Call either inline onclick or item href

      if ($item.data("onclick")) $item.data("onclick")();
      else window.location = $item.attr("href");
    },

    toggle: function($item) {
      this[$item.hasClass("open") ? "hide" : "show"]($item);
    },

    show: function($item) {
      var that = this;
      var parent = $item.parent();
      var collapsible = $item.next();

      if (this.options.onlyOneShown)
        // Hide other opened menu

        this.hide(parent.siblings().find("> .open"));

      $item.addClass("open");
      $item.prev().addClass("opened");
      collapsible.slideDown({
        complete: function() {
          if (that.options.autoScroll) that.focusItem($item);
        }
      });
    },

    hide: function($item) {
      var collapsible = $item.next();
      var activatedCollapsible = collapsible.find(".open");
      $item.removeClass("open");
      $item.prev().removeClass("opened");
      collapsible.slideUp({
        complete: function() {
          //   Collapse all sub items which have 'open' class

          activatedCollapsible
            .removeClass("open")
            .next()
            .hide();
          activatedCollapsible.prev().removeClass("opened");
        }
      });
    },

    focusItem: function($item) {
      var windowScrollTop = $(window).scrollTop();
      var targetScrollTop = $item.offset().top;

      // Avoid downward direction auto scroll focus

      if (targetScrollTop < windowScrollTop) {
        setTimeout(function() {
          $("html, body").animate(
            {
              scrollTop: targetScrollTop
            },
            500
          );
        }, 50);
      }
    }
  };

  $.fn.accordionMenu = function(option) {
    return this.each(function() {
      var $this = $(this);
      var data = $this.data("AccordionMenu");
      var options = $.extend(
        {},
        AccordionMenu.DEFAULTS,
        typeof option == "object" && option
      );

      // Avoid multiple intentiation on the same elment

      if (!data)
        $this.data("AccordionMenu2", (data = new AccordionMenu(this, options)));
    });
  };
})(jQuery);
