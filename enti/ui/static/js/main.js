require.config({
	paths: {
		domReady: '../lib/domReady/domReady',
		angular: '../lib/angular/angular',
		angularMoment: '../lib/angular-moment/angular-moment',
		'angular-moment': '../lib/angular-moment/angular-moment',
		bootstrap: '../lib/bootstrap/dist/js/bootstrap',
		'jquery.easing': '../lib/jquery-easing/jquery.easing.min',
		mixitup: '../lib/mixitup/src/jquery.mixitup',
		moment: '../lib/moment/moment',
		requirejs: '../lib/requirejs/require',
		retinajs: '../lib/retinajs/dist/retina',
		'socket.io': '../lib/socket.io-client/dist/socket.io.min',
		velocity: '../lib/velocity/velocity',
		'velocity.ui': '../lib/velocity/velocity.ui',
		'please-wait': '../lib/please-wait/build/please-wait',
		jquery: '../lib/jquery/dist/jquery',
		notify: '../lib/remarkable-bootstrap-notify/bootstrap-notify',
		'remarkable-bootstrap-notify': '../lib/remarkable-bootstrap-notify/bootstrap-notify',
		'angular-animate': '../lib/angular-animate/angular-animate',
		'bs-switch': '../lib/angular-bootstrap-switch/dist/angular-bootstrap-switch'
	},
	shim: {
		angular: {
			exports: 'angular'
		},
		'angular-animate': {
			exports: 'ngAnimate',
			deps: ['angular']
		}
	},
	deps: [
		'../js/bootstrap'
	],
	packages: [
		{
			name: 'moment',
			location: '../lib/moment',
			main: 'moment'
		}
	]
});

require(['socket.io'], function (io) {
	console.log('Socket.IO Connection:' + location.protocol + '//' + document.domain + ':' + window.location.port + '/');
	window.socket = io.connect(location.protocol + '//' + document.domain + ':' + window.location.port + '/', {
		reconnect: true,
		transports: ['websocket', 'polling']
	});
	socket.on('connect', function () {
		console.log('Socket.IO Connected');
	});
});