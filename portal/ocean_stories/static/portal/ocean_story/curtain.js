var bindCurtain = function(elements, isCollapsed) {
  var learnMoreHeight,
      viewHeight,
      startHeight,
      endHeight,
      state,
      ticking,
      needResize;

  function requestTick(resize) {
    if(!ticking) {
      requestAnimationFrame(update);
    }
    ticking = true;
    if (resize) {
      needResize = true;
    }
  }

  function update() {
    ticking = false;

    if (needResize = true) {
      needResize = false;
      learnMoreHeight = $('.learn-more').height();
      viewHeight = $( this ).height();
      startHeight = viewHeight - learnMoreHeight;
      endHeight = viewHeight/2;
    }

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
    requestTick(true);
  }
  onResize();
  $(window).scroll(requestTick);
  $(window).resize(onResize);

}

module.exports = bindCurtain;
