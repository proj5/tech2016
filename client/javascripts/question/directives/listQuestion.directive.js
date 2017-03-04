(function () {
  'use strict';

  angular
    .module('tech2016.question.directives')
    .directive('a2aListQuestion', ListQuestionDirective);

    ListQuestionDirective.$inject = [];

    function ListQuestionDirective() {
      return {
        restrict: 'E',
        scope: {},
        bindToController: {
          urlNextQuestion: '='
        },
        controller: 'ListQuestionController',
        controllerAs: 'vm',
        templateUrl: 'client/templates/ListQuestion.html'
      };
    }
})();
