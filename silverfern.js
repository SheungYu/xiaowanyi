var casper = require('casper').create({
	pageSettings: {
        loadImages:  false,        // The WebPage instance used by Casper will
        loadPlugins: false         // use these settings
    },
    logLevel: "info",              // Only "info" level messages will be logged
    verbose: true                  // log messages will be printed out to the console
});

var LOGIN_URL = 'https://www.immigration.govt.nz/secure/Login+Silver+Fern.htm'
var SILVERFERN_URL = 'https://www.immigration.govt.nz/SilverFern/'
var LOGIN_USER = ''
var LOGIN_PASS = ''

casper.start(LOGIN_URL);

casper.waitForSelector('form#Login',
	function then() {
		 this.fill('form#Login', {
			'OnlineServicesLoginStealth:VisaLoginControl:userNameTextBox':    LOGIN_USER,
			'OnlineServicesLoginStealth:VisaLoginControl:passwordTextBox':    LOGIN_PASS,
		}, true);
		this.click('input#OnlineServicesLoginStealth_VisaLoginControl_loginImageButton');
	},
	function onTimeout() {
		this.die('Timeout when open login page', -1)
	}
)

casper.waitFor(function check() {
		return this.getTitle().indexOf("homepage")>-1;
	}, 
	function then() {
		this.echo("登录成功!!!!!!!!!!!!");
	},
	function timeout() {
		this.die('Timeout when submit login', -1)
	}
)

casper.thenOpen(SILVERFERN_URL, function() {
	if(this.getTitle() == 'Runtime Error') {
		this.echo("Runtime Error")
	}
	
	var text = this.fetchText('body');

	if(text.indexOf('Unfortunately at this time we are not accepting new applications') > -1) {
		this.echo("Congratulations, you got it!")
		this.echo(text)
	}
});

casper.run();
