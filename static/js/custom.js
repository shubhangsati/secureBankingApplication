$('.button-collapse').sideNav({
      menuWidth: 240, // Default is 240
      closeOnClick: true // Closes side-nav on <a> clicks, useful for Angular/Meteor
    }
  );


$(document).ready(function() {
        $('select').material_select();
});

// Show sideNav
  $('.button-collapse').sideNav('show');
  // Hide sideNav
  $('.button-collapse').sideNav('hide');
        