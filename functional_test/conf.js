// conf.js
config = {
  framework: 'jasmine',
  seleniumAddress: 'http://localhost:4444/wd/hub',
  specs: ['spec.js'],  
}

if (process.env.TRAVIS) config.capabilities = {'browserName': 'firefox', }
exports.config = config
