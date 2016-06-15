describe('Log in', function() {
  
  beforeEach(function() {
    browser.get('http://localhost:8000/');
  });
  
  it('should register', function() {        
    element(by.linkText('Register')).click();
    
    element(by.model('vm.username')).sendKeys('abc');
    element(by.model('vm.password')).sendKeys('defg1234');
    element(by.model('vm.confirmPassword')).sendKeys('defg1234');
    element(by.model('vm.email')).sendKeys('abc@123.com');
    element(by.model('vm.firstName')).sendKeys('A');
    element(by.model('vm.lastName')).sendKeys('B');
    
    element(by.buttonText('Register')).click();
    
    browser.driver.wait(function() {
      return browser.driver.getCurrentUrl().then(function(url) {
        return /newsfeed/.test(url);
      });
    }, 10000);
  });
  
  //*
  it('should log out', function() {            
    element(by.id('dropdownMenu1')).click();
    element(by.linkText('Log out')).click();
    browser.driver.wait(function() {
      return browser.driver.getCurrentUrl().then(function(url) {
        return /newsfeed/.test(url);
      });
    }, 10000);
  });   
});
