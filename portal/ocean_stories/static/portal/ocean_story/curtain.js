var bindCurtain = function(elements, isCollapsed) {
  var learnMoreHeight,
      viewHeight,
      startHeight,
      endHeight,
      state,
      ticking,
      needResize;

  function requestTick() {
    if(!ticking) {
      requestAnimationFrame(update);
    }
    ticking = true;
  }

  function update() {
    ticking = false;

    state = calcState(startHeight, endHeight);

    elements.height(state.height);
    isCollapsed(state.collapsed);
  }

  var calcState = function(startHeight, endHeight){
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

  var onResize = function(){
    // immediate update onResize
    learnMoreHeight = $('.learn-more').height();
    viewHeight = $( this ).height();
    startHeight = viewHeight - learnMoreHeight;
    endHeight = viewHeight/2;
    update();
  }
  onResize();
  $(window).scroll(requestTick);
  $(window).resize(onResize);

}

module.exports = bindCurtain;
