define([
	'angular',
	'./services/index',
	'./controllers/index',
	'./filters/index'
], function (ng) {
	'use strict';

	return ng.module('app', [
	    'angularFileUpload',
		'app.controllers',
		'app.filters',
		'app.services',
		'angularMoment',
		'ngAnimate'
	]).config(['$interpolateProvider', function ($interpolateProvider) {
		$interpolateProvider.startSymbol('{a').endSymbol('a}');
	}]);
});
