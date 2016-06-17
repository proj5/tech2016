(function () {
  'use strict';

  angular
    .module('tech2016.topic.controllers')
    .controller('ListTopicController', ListTopicController);

    ListTopicController.$inject = ['$http', '$state', '$stateParams', 'TopicService'];

  function ListTopicController($http, $state, $stateParams, TopicService) {
    var vm = this;        
    
    TopicService.getListTopic(function assignListTopic(data){
      vm.listTopic = data;
    });
  }
})();
