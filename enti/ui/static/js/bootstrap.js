define([
	'require',
	'angular',
	'moment',
	'angular-animate',
	'angularMoment',
	'notify',
	'app'
	/* routes */
], function (require, ng) {
	'use strict';


	require(['domReady!'], function (document) {
		ng.bootstrap(document, ['app']);
	});
});

