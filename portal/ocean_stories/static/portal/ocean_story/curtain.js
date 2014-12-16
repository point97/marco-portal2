var bindCurtain = function(elements, isCollapsed) {
  var learnMoreHeight;
  var viewHeight;
  var startHeight;
  var endHeight;

  var calcHeight = function(){
    var scrollTop = $(this).scrollTop();
    var proportion = scrollTop/(startHeight - endHeight);
    if (proportion <= 0) {
      isCollapsed(false);
      return startHeight;
    }
    if (proportion <= 1) {
      isCollapsed(false);
      return endHeight*proportion + startHeight*(1-proportion);
    }
    isCollapsed(true);
    return endHeight;
  };
  var setHeight = function() {
    var curtainHeight = calcHeight();
    elements.height(curtainHeight);
  };

  var handleResize = function(){
    learnMoreHeight = $('.learn-more').height();
    viewHeight = $( this ).height();
    startHeight = viewHeight - learnMoreHeight;
    endHeight = viewHeight/2;
    setHeight();
  }
  handleResize();
  $(window).scroll(setHeight);
  $(window).resize(handleResize);

}

module.exports = bindCurtain;
