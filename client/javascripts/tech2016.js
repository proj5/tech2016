(function () {
  'use strict';

  angular
    .module('tech2016', [
      'tech2016.config',
      'tech2016.routes',
      'tech2016.users',
      'tech2016.main',
      'tech2016.questions'
  ]);

  angular
    .module('tech2016')
    .run(run);

  run.$inject = ['$http'];

  /**
  * @name run
  * @desc Update xsrf $http headers to align with Django's defaults
  */
  function run($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }

  angular
    .module('tech2016.routes', [
      'ui.router'
    ]);

  angular
    .module('tech2016.config', []);
})();
