function bind(navbar) {
  var searchDropdown = navbar.find('.search-dropdown');
  navbar.find('.search-dropdown').on('shown.bs.dropdown', function () {
    $( this ).find('input.search-input').focus();
  }).find('form').keyup(function(e) {
    if (e.keyCode == 27) {
      e.preventDefault();
      e.stopPropagation();
      // maybe this should be a different event, but this seems to work
      $(document).trigger('click.bs.dropdown.data-api');
    }
  }).each(function(i,elt){elt.reset()});
};

module.exports = bind;
