describe('newsfeed', function() { 
  
  it('should log in', function() {   
    browser.get('http://localhost:8000/');
    element(by.model('vm.username')).sendKeys('quang');
    element(by.model('vm.password')).sendKeys('admin123');    
    
    element(by.buttonText('Login')).click();
    
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
    
    expect(element(by.buttonText('Login')).isPresent()).toBeTruthy();
  });   
});
