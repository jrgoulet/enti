define(['./module'], function (services) {
	'use strict';
	services.factory('NotificationSvc', function () {

		var template = {
			'default': '<div data-notify="container" class="col-xs-3 alert alert-{0} wrap" role="alert">' +
			'<button type="button" class="close text-dark" style="width:20px;" data-notify="dismiss">×</button>' +
			'<span data-notify="text-dark icon" class="s21" style="width:40px;"></span><span class="text-dark s15 s500" data-notify="title">{1}</span>:&nbsp;' +
			'<span class="text-dark s15 s300" data-notify="message" style="padding-left: 10px;">{2}</span></div>',

			'live': '<div data-notify="container" class="col-xs-3 alert alert-{0} wrap" role="alert">' +
			'<button type="button" class="close text-dark" style="width:20px;" data-notify="dismiss">×</button>' +
			'<div class="col-xs-2"><div class="sk-fading-circle" style="height: 60px; width: 35px;">' +
			'<div class="sk-circle1 sk-circle"></div><div class="sk-circle2 sk-circle"></div>' +
			'<div class="sk-circle3 sk-circle"></div><div class="sk-circle4 sk-circle"></div>' +
			'<div class="sk-circle5 sk-circle"></div><div class="sk-circle6 sk-circle"></div>' +
			'<div class="sk-circle7 sk-circle"></div><div class="sk-circle8 sk-circle"></div>' +
			'<div class="sk-circle9 sk-circle"></div><div class="sk-circle10 sk-circle"></div>' +
			'<div class="sk-circle11 sk-circle"></div><div class="sk-circle12 sk-circle"></div></div></div>' +
			'<div class="col-xs-10"><span class="text-dark s15 s500" data-notify="title">{1}</span>:&nbsp;' +
			'<span class="text-dark s15 s300" data-notify="message" style="padding-left: 10px;">{2}</span></div></div>'
		};

		$.notifyDefaults({
			element: 'body',
			allow_dismiss: true,
			newest_on_top: true,
			showProgressbar: false,
			url_target: '_blank',
			icon_type: 'class',
			template: template.default,
			placement: {
				from: "bottom",
				align: "left"
			},
			animate: {
				enter: 'animated fadeInDown',
				exit: 'animated fadeOutUp'
			}
		});

		var success = function (title, message) {
			var options = {
				icon: 'fa fa-info-circle',
				title: title,
				message: message
			};
			var settings = {
				type: 'success'
			};
			$.notify(options, settings);
		};
		var info = function (title, message) {
			var options = {
				icon: 'fa fa-info-circle',
				title: title,
				message: message
			};
			var settings = {
				type: 'info'
			};
			$.notify(options, settings);
		};
		var warning = function (title, message) {
			var options = {
				icon: 'fa fa-warning',
				title: title,
				message: message
			};
			var settings = {
				type: 'warning'
			};
			$.notify(options, settings);
		};
		var danger = function (title, message) {
			var options = {
				icon: 'fa fa-warning',
				title: title,
				message: message
			};
			var settings = {
				type: 'danger'
			};
			$.notify(options, settings);
		};
		var progress = function (title, message) {
			var options = {
				title: title,
				message: message
			};
			var settings = {
				template: template.live,
				delay: 25000
			};
			return $.notify(options, settings);
		};

		return {
			success: success,
			info: info,
			warning: warning,
			danger: danger
		};

	})
});