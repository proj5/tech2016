(function () {
  'use strict';

  angular
    .module('tech2016.question.controllers')
    .controller('QuestionController', QuestionController);

    QuestionController.$inject = ['$scope', '$state', '$http', '$stateParams'];

    function QuestionController($scope, $state, $http, $stateParams) {
      var vm = this;
      vm.questionID = $stateParams.questionID;
      init();

      function init() {
        //http://localhost:8000/api/v1/question/?questionID=1
        vm.url = "api/v1/question/?questionID=" + vm.questionID;
        $http.get(vm.url)
        .then(function successCallback(response){
            vm.question = response.data;
        }, function errorCallback(response) {
            console.log("Error get question");
        });
      }
    }
})();
