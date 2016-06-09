(function () {
  'use strict';

  angular
    .module('tech2016.questions.controllers')
    .controller('QuestionsController', QuestionsController);

    QuestionsController.$inject = ['$scope', '$state', 'Authentication'];

    function QuestionsController($scope, $state, Authentication) {
      var vm = this;
    }
})();
