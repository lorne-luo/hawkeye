(function($) {
  "use strict";

  var site = (window.site = {});

  site.elements = {
    menu: $(".menu-hamburger"),
    sideMenu: $(".menu-side"),
    btnMenu: $(".btn-menu"),
    hamburgerMenu: $(".page-head-bottom-menus"),
    pageHead: "page-head"
  };

  site.getBreakpoint = (function() {
    var breakpoint;

    function getBreakpointContent() {
      return window
        .getComputedStyle(document.body, ":after")
        .content.toLowerCase()
        .replace(/\"/g, "");
    }

    breakpoint = getBreakpointContent();
    $(window).resize(function() {
      breakpoint = getBreakpointContent();
    });

    return function() {
      return breakpoint;
    };
  })();

  /* Generate overlay */

  site.showDrawerOverlay = function() {
    $("body").addClass("toggled-drawer-offset-overlay");
  };

  site.hideDrawerOverlay = function() {
    $("body").removeClass("toggled-drawer-offset-overlay");
  };

  /* End of Generating overlay */

  /* Initializing shadow scroller */

  site.shadowScroller = function() {
    $(".item-page table").shadowScroller();
  };

  /* End of initializing shadow scroller */

  /* Reset rs form submit button when clickout outside of recaptcha */

  site.recaptcha = function() {
    $(document).mouseup(function(e) {
      var iframe = $('iframe[title="recaptcha"]');

      // if the target of the click outside of the recaptcha iframe

      if (!iframe.is(e.target) && iframe.has(e.target).length === 0) {
        $(".rsform-submit-button").each(function() {
          if ($(this).prop("disabled")) {
            $(this).removeProp("disabled");
          }
        });
      }
    });
  };

  /* End of reset rs form submit button when clickout outside of recaptcha */

  /* Initializing dropdown menu */

  site.accordionMenu = function(menu) {
    $(menu).accordionMenu({
      addIndicator: true,
      onlyOneShown: true,
      autoScroll: true
    });
  };

  /* End of Initializing dropdown menu */

  /* Hamburger menu */

  site.hamburgerMenu = {
    isActive: false,

    close: function() {
      site.elements.hamburgerMenu.removeClass("active");
      site.elements.btnMenu.removeClass("active");
      site.hideDrawerOverlay();
      this.isActive = false;
    },

    open: function() {
      site.elements.hamburgerMenu.addClass("active");
      site.elements.btnMenu.addClass("active");
      site.showDrawerOverlay();
      this.isActive = true;
    },

    init: function() {
      var that = this;

      site.elements.btnMenu.click(function(e) {
        e.preventDefault();
        that.isActive ? that.close() : that.open();
      });

      $(document).on("click touchend", function(e) {
        if (
          !$(e.target).closest("." + site.elements.pageHead).length &&
          that.isActive
        ) {
          that.close();
        }
      });

      $(window).on("resize", function() {
        if (site.getBreakpoint() === "desktop" && that.isActive) {
          that.close();
        }
      });
    }
  };

  /* End of hamburger menu */

  /* Content Accodion */

  site.accordion = function() {
    $(".accordion-item__body").hide();
    $(".accordion-item__body").attr("aria-hidden", "true");
    $("a.accordion-item__title-container").addClass(
      "accordion-item__title-container--toggle-off"
    );
    $("a.accordion-item__title-container--toggle-off").attr(
      "aria-seleted",
      "false"
    );

    /** Adding aria-control div id**/

    var itemNum = 1;
    $(".accordion-item").each(function() {
      var accordionIDName = "accordionietm-" + itemNum;
      $(this)
        .find(".accordion-item__title-container")
        .attr("aria-controls", accordionIDName);
      $(this)
        .find(".accordion-item__body")
        .attr("id", accordionIDName);
      itemNum++;
    });

    $("a.accordion-item__title-container").on("click", function() {
      // Prevent clicks upon animation

      if ($(".accordion-item__body :animated").length) return false;

      if ($(this).hasClass("accordion-item__title-container--toggle-on")) {
        $(this)
          .parent()
          .next(".accordion-item__body")
          .attr("aria-hidden", "true")
          .slideUp();
        $(this).removeClass("accordion-item__title-container--toggle-on");
        $(this).addClass("accordion-item__title-container--toggle-off");
        $(this).attr("aria-seleted", "false");
      } else {
        $(".accordion-item__body").slideUp();
        $(this)
          .parent()
          .next(".accordion-item__body")
          .attr("aria-hidden", "false")
          .slideDown();
        $("a.accordion-item__title-container").removeClass(
          "accordion-item__title-container--toggle-on"
        );
        $("a.accordion-item__title-container").addClass(
          "accordion-item__title-container--toggle-off"
        );
        $(this).removeClass("accordion-item__title-container--toggle-off");
        $(this).addClass("accordion-item__title-container--toggle-on");
        $(this).attr("aria-seleted", "true");
      }

      return false;
    });
  };

  /* End of content accordion*/

  site.init = function() {
    site.shadowScroller();
    site.recaptcha();
    site.accordionMenu(site.elements.menu);
    site.accordionMenu(site.elements.sideMenu);
    site.hamburgerMenu.init();
    site.accordion();
  };

  // Document ready

  $(function() {
    site.init();
  });
})(jQuery);
