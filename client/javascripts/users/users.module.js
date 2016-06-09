(function () {
  'use strict';

  angular
    .module('tech2016.users', [
      'tech2016.users.controllers',
      'tech2016.users.services'
    ]);

  angular
    .module('tech2016.users.controllers', []);

  angular
    .module('tech2016.users.services', [
      'ngCookies'
    ]);
})();