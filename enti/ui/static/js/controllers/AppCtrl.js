define(['./module'], function (controllers) {
    'use strict';

    controllers.controller('AppCtrl', ['$rootScope', '$http', '$scope', '$window', 'moment', 'IOSvc', 'AttributeSvc',
		'NotificationSvc', 'FileUploader',
        function ($rootScope, $http, $scope, $window, moment, io, attrSvc, n, FileUploader) {

            console.log('AppCtrl');

            $scope.attributes = {};
            $scope.view = 'default';
            $scope.uploader = new FileUploader();

            $scope.uploader.onAfterAddingFile = function(file) {
               console.log('File added');
               console.log(file);
            };

            $scope.uploader.onErrorItem = function(item, response, status, headers) {
               item.remove();
               n.warning('Upload failed', 'Ensure that the file is a valid XML file.')
            };

            $scope.uploader.onSuccessItem = function(item, response, status, headers) {
                item.remove();
                n.info('Upload successful', 'The XML file has been uploaded successfully.');
                io.emit('xml.upload', null)
            };


            $scope.setView = function(view) {
                console.log('View set to ' + view);
                $scope.view = view;
            };

            $scope.route = {
                add: function (source_id, cage_id) {
                    routeSvc.add(source_id, cage_id)
                },
                remove: function (source_id, cage_id) {
                    routeSvc.remove(source_id, cage_id);
                }
            };

            $scope.action = {
                locate: function (id) {
                    actionSvc.locate(id)
                }
            };

            $scope.util = {
                isEmpty: function (dict) {
                    if (dict !== null && typeof dict === 'object') {
                        return Object.keys(dict).length === 0;
                    }
                    return true
                }
            };

            io.on('attribute.sync', function(attributes) {
               $scope.attributes = attrSvc.sync(attributes);
            });

            io.on('success', function (message) {
                console.log('success: ' + message.message);
                n.info(message.title, message.message);
            });

            io.on('info', function (message) {
                console.log('info: ' + message.message);
                n.info(message.title, message.message);
            });

            io.on('warning', function (message) {
                console.log('warning: ' + message.message);
                n.warning(message.title, message.message);
            });

            io.on('danger', function (message) {
                console.log('danger: ' + message.message);
                n.danger(message.title, message.message);
            });

            //////////////////////////////////////////////////

            io.emit('attribute.sync', null);

        }])
});