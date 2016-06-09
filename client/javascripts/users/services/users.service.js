(function () {
  'use strict';

  angular
    .module('tech2016.users.services')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http'];

  function Authentication($cookies, $http) {

    var Authentication = {
      getAuthenticatedAccount: getAuthenticatedAccount,
      isAuthenticated: isAuthenticated,
      register: register,
      setAuthenticatedAccount: setAuthenticatedAccount,
      unauthenticate: unauthenticate,
      login: login,
      logout: logout
    };

    return Authentication;

    ////////////////////

    /*
    * @name register
    * @desc Try to register a new user
    * @param {string} username The username entered by the user
    * @param {string} password The password entered by the user
    * @param {string} email The email entered by the user
    * @returns {Promise}
    */
    function register(username, password, confirm_password, email, first_name, last_name) {
      return $http({
        method: 'POST',
        url: '/api/v1/accounts/',
        data: {
          user:{
            username: username,
            password: password,
            confirm_password: confirm_password,
            email: email,
            first_name: first_name,
            last_name: last_name
          }
        },
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(registerSuccessFn, registerErrorFn);

      /**
      * @name registerSuccessFn
      * @desc Log the new user in
      */
      function registerSuccessFn(data, status, headers, config) {
        Authentication.login(username, password);
      }

      /**
      * @name registerErrorFn
      * @desc Log "Epic failure!" to the console
      */
      function registerErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }


    function login(username, password) {
      return $http({
        method: 'POST',
        url: '/api/v1/auth/login/',
        data: {
          username: username,
          password: password
        },
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(loginSuccessFn, loginErrorFn);

      /**
       * @name loginSuccessFn
       * @desc Set the authenticated account and redirect to index
       */
      function loginSuccessFn(data, status, headers, config) {
        Authentication.setAuthenticatedAccount(data.data);
        window.location = '/newsfeed';
      }

      /**
       * @name loginErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function loginErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }

    /**
     * @name logout
     * @desc Try to log the user out
     * @returns {Promise}
     */
    function logout() {
      return $http.post('/api/v1/auth/logout/')
        .then(logoutSuccessFn, logoutErrorFn);

      /**
       * @name logoutSuccessFn
       * @desc Unauthenticate and redirect to index with page reload
       */
      function logoutSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();
        window.location = '/';
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function logoutErrorFn(data, status, headers, config) {
        console.error('Logout Error');
      }
    }

    function getAuthenticatedAccount() {
      if (!$cookies.get('authenticatedAccount')) {
        return;
      }

      return JSON.parse($cookies.get('authenticatedAccount'));
    }

    function isAuthenticated() {
      return $cookies.get('authenticatedAccount');
    }

    /**
     * @name setAuthenticatedAccount
     * @desc Stringify the account object and store it in a cookie
     * @param {Object} user The account object to be stored
     * @returns {undefined}
     */
    function setAuthenticatedAccount(account) {
      $cookies.put('authenticatedAccount', JSON.stringify(account));
    }

    /**
     * @name unauthenticate
     * @desc Delete the cookie where the user object is stored
     * @returns {undefined}
     */
    function unauthenticate() {
      $cookies.remove('authenticatedAccount');
    }

  }
})();