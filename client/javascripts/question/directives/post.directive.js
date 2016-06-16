(function () {
  'use strict';

  angular
    .module('tech2016.question.directives')
    .directive('a2aPost', PostDirective);

    PostDirective.$inject = [];

    function PostDirective() {
      return {
        restrict: 'E',
        scope: {},
        bindToController: {
          name: '@',
          post: '=',
          parentController: '=',
          showComment: '@'
        },
        controller: 'PostController',
        controllerAs: 'vm',
        templateUrl: 'client/templates/Post.html'
      };
    }
})();
