(function () {
  'use strict';

  angular
    .module('tech2016.topic.controllers')
    .controller('TopicController', TopicController);

    TopicController.$inject = ['$http', '$state', '$stateParams', 'TopicService'];

  function TopicController($http, $state, $stateParams, TopicService) {
    var vm = this;        
    
    vm.topicID = $stateParams.topicID;
    vm.urlNextQuestion = 'api/v1/topic/question/?topicID=' + vm.topicID;
    TopicService.getTopic(vm.topicID, function assignTopic(data){
      vm.topic = data;
      TopicService.getRelatedTopic(vm.topic.name, function assignRelatedTopic(data){
        vm.relatedTopic = data;
      });
      
    });
  }
})();
