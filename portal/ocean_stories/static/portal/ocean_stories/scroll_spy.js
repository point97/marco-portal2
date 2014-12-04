/**
 * Binds a scroll listener to window.
 * Calls callback with selector index whenever scroll position
 * transitions between sections.
 *
 * @param {array} selector jQuery selector defining page sections
 * @return {Object} with off() method.
 */
function scrollSpy(containerSelector, sectionSelector, callback) {
  var container = $(containerSelector);
  var sections = container.find(sectionSelector);
  var currentIndex;
  var fuzz = 10;

  function handleScroll() {
    // Get container scroll position
    var topMargin = parseInt(container.css('margin-top'));
    var contentScrollTop = $(this).scrollTop() + topMargin;

    var sectionIndex = _.findLastIndex(sections, function(s){
      return $(s).offset().top - fuzz < contentScrollTop;
    })

    if (sectionIndex !== currentIndex) {
      callback(sectionIndex);
    }
  }

  handleScroll.call(window)
  $(window).scroll(handleScroll);
}
