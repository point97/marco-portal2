var bindCurtain = function(elements, isCollapsed) {
  var learnMoreHeight;
  var viewHeight;
  var startHeight;
  var endHeight;

  var calcState = function(){
    var scrollTop = $(this).scrollTop();
    var proportion = scrollTop/(startHeight - endHeight);
    var collapsed;
    var height;

    return (proportion <= 0) ? {
      collapsed: false,
      height: startHeight
    } : (proportion <= 1) ? {
        collapsed: false,
        height: endHeight*proportion + startHeight*(1-proportion)
    } : {
      height: endHeight,
      collapsed: true
    }
  };
  var setState = function() {
    var newState = calcState();
    elements.height(newState.height);
    isCollapsed(newState.collapsed);
  };

  var handleResize = function(){
    learnMoreHeight = $('.learn-more').height();
    viewHeight = $( this ).height();
    startHeight = viewHeight - learnMoreHeight;
    endHeight = viewHeight/2;
    setState();
  }
  handleResize();
  $(window).scroll(setState);
  $(window).resize(handleResize);

}

module.exports = bindCurtain;
