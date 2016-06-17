(function () {
  'use strict';

  angular
    .module('tech2016.topic.controllers')
    .controller('TopicController', TopicController);

    TopicController.$inject = ['$http', '$state', '$stateParams'];

  function TopicController($http, $state, $stateParams) {
    var vm = this;    
    
    vm.topicID = $stateParams.topicID;
    vm.urlNextQuestion = 'api/v1/topic/question/?topicID=' + vm.topicID;    
  }
})();
