(function () {
  'use strict';

  angular
    .module('tech2016.question.controllers')
    .controller('QuestionController', QuestionController);

    QuestionController.$inject = ['$scope', '$state', 'Authentication'];

    function QuestionController($scope, $state, Authentication) {
      var vm = this;
    }
})();
