define(['./module'], function (controllers) {
    'use strict';

    controllers.controller('AppCtrl', ['$rootScope', '$http', '$scope', '$window', 'moment', 'IOSvc', 'AttributeSvc',
        'EntitySvc', 'NotificationSvc', 'FileUploader',
        function ($rootScope, $http, $scope, $window, moment, io, attrSvc, entitySvc, n, FileUploader) {


            $scope.view = 'default';
            /**
             * Sets the main view
             * @param view The name of the view
             */
            $scope.setView = function (view) {
                console.log('View set to ' + view);
                $scope.view = view;
            };

            //////////////////////////////////////////////////

            $scope.form = {
                hover: {},
                attribute: {
                    edit: {},
                    new: {},
                    expanded: {}
                },
                entity: {
                    expanded: {},
                    edit: {},
                    new: {}
                },
                expanded: {},
                property: {},
                add: {
                    entity: {
                        id: null,
                        name: null,
                        type: null,
                        canonical: true,
                        expanded: false
                    }
                },
                import: {
                    expanded: false
                },
                remove: {
                    entity: {
                        expanded: {}
                    }
                },
                settings: {
                    source: {
                        expanded: false
                    }
                }
            };
            $scope.hover = {};

            //////////////////////////////////////////////////

            $scope.uploader = new FileUploader();

            /**
             * Callback used after adding a file to the upload queue
             * @param file The file added to the queue
             */
            $scope.uploader.onAfterAddingFile = function (file) {
                console.log('File added');
                console.log(file);
            };

            /**
             * Callback used after an upload fails
             * @param item The item that failed to upload
             * @param response The response given by the controller
             * @param status The response status
             * @param headers Response headers
             */
            $scope.uploader.onErrorItem = function (item, response, status, headers) {
                item.remove();
                n.warning('Upload failed', 'Ensure that the file is a valid XML file.')
            };

            /**
             * Callback used after successfully uploading an item
             * @param item The item
             * @param response The response given by the controller
             * @param status The response status
             * @param headers Response headers
             */
            $scope.uploader.onSuccessItem = function (item, response, status, headers) {
                item.remove();
                n.info('Upload successful', 'The XML file has been uploaded successfully.');
                io.emit('xml.upload', null)
            };

            //////////////////////////////////////////////////

            $scope.entities = {};
            $scope.entityTypes = {};
            $scope.entitySvc = entitySvc;
            $scope.entityFilter = 'all';
            $scope.selectedEntity = null;
            $scope.entity = {
                init: {
                    /**
                     * Navigate to the add entity view
                     */
                    add: function () {
                        $scope.view = 'add';
                        $scope.form.add.entity.expanded = true;
                    },
                    /**
                     * Navigate to the import entity view
                     */
                    import: function () {
                        $scope.view = 'import';
                        $scope.selectedEntity = null;
                    },
                    /**
                     * Initialize editor form for entity properties
                     * @param entityId The ID of the entity being modified
                     */
                    props: function (entityId) {
                        $scope.form.property[entityId] = {
                            id: {
                                hover: false,
                                expanded: false,
                                edit: null
                            },
                            name: {
                                hover: false,
                                expanded: false,
                                edit: null
                            },
                            type: {
                                hover: false,
                                expanded: false,
                                edit: null
                            },
                            canonical: {
                                hover: false,
                                expanded: false,
                                edit: null
                            }
                        }
                    },
                    edit: {
                        /**
                         * Initialize the field editor for an entity property
                         * @param entityId The ID of the entity being modified
                         * @param property The property being modified
                         */
                        props: function (entityId, property) {
                            $scope.form.property[entityId][property].expanded = true;
                            $scope.form.property[entityId][property].edit = $scope.entities[entityId][property];
                        }
                    }
                },
                /**
                 * Select an entity to view/edit details
                 * @param entityId The ID of the entity to inspect
                 */
                select: function (entityId) {
                    console.log('Selecting entity:' + entityId);
                    $scope.view = 'entity';
                    $scope.selectedEntity = entityId;
                    $scope.entity.init.props(entityId);
                },
                /**
                 * Export all entities
                 */
                export: function () {
                    n.info('Export', 'Preparing entities for export');
                    io.emit('entity.export.all', null);
                },
                add: {
                    /**
                     * Add an entity
                     */
                    submit: function () {
                        io.emit('entity.add', {
                            id: $scope.form.add.entity.id,
                            name: $scope.form.add.entity.name,
                            type: $scope.form.add.entity.type,
                            canonical: $scope.form.add.entity.canonical
                        });
                        $scope.form.add.entity.expanded = false;
                    },
                    /**
                     * Add entity failure callback
                     * Prompts user for another attempt
                     */
                    reattempt: function () {
                        $scope.form.add.entity.expanded = true;
                        n.warning('Add Entity', 'Please check new entity data and try again.');
                    },
                    /**
                     * Add entity success callback
                     * Resets the add entity form
                     */
                    confirm: function () {
                        $scope.form.add.entity.id = null;
                        $scope.form.add.entity.name = null;
                        $scope.form.add.entity.type = null;
                        $scope.form.add.entity.canonical = true;
                    }
                },
                /**
                 * Update an entity
                 * @param entityId The ID of the entity
                 * @param property The property (name, type, canonical) to modify
                 */
                update: function (entityId, property) {
                    var entity = {
                        id: $scope.entities[entityId].id,
                        name: $scope.entities[entityId].name,
                        type: $scope.entities[entityId].type,
                        canonical: $scope.entities[entityId].canonical
                    };
                    entity[property] = $scope.form.property[entityId][property].edit;
                    io.emit('entity.update', entity);
                    $scope.form.property[entityId][property].expanded = false;
                },
                /**
                 * Remove an entity
                 * @param entityId The ID of the entity
                 */
                remove: function (entityId) {
                    io.emit('entity.remove', {
                        id: entityId
                    });
                    $scope.selectedEntity = null;
                    delete $scope.entities[entityId];
                    delete entitySvc.entities[entityId];
                },
                /**
                 * Filters entities
                 * Set by 1st column, displayed in 2nd column
                 * @param filter
                 */
                filter: function (filter) {
                    console.log('Filter set to ' + filter);
                    $scope.entityFilter = filter;
                }
            };

            //////////////////////////////////////////////////

            $scope.attributes = {};
            $scope.attrSvc = attrSvc;
            $scope.source = 'default';
            $scope.attribute = {
                init: {
                    /**
                     * Initialize the Add Attribute form for the editor
                     * @param entityId The ID of the entity to modify
                     */
                    add: function (entityId) {
                        $scope.form.attribute.new[entityId] = {
                            attributeId: null,
                            fields: {}
                        };
                    },
                    /**
                     * Initialize an EntityAttributeField form for editing
                     * @param fieldId The ID of the EntityAttributeField to modify
                     */
                    update: function (fieldId) {
                        if ($scope.form.attribute.edit[fieldId] == null) {
                            $scope.form.attribute.edit[fieldId] = {
                                expanded: false,
                                value: null
                            };
                        }
                    }
                },
                /**
                 * Add an attribute to an entity
                 * @param entityId The ID of the entity to modify
                 */
                add: function (entityId) {
                    console.log('Add attribute: ' + entityId + ', ' + $scope.form.attribute.new[entityId].attributeId);
                    console.log($scope.form.attribute.new[entityId].fields);
                    io.emit('attribute.add', {
                        entityId: entityId,
                        attributeId: $scope.form.attribute.new[entityId].attributeId,
                        fields: $scope.form.attribute.new[entityId].fields
                    });
                    $scope.attribute.init.add(entityId);
                },
                /**
                 * Remove an attribute from an entity
                 * @param entityId The ID of the entity to modify
                 * @param attributeId The ID of the EntityAttribute to remove
                 */
                remove: function (entityId, attributeId) {
                    console.log('Remove attribute: ' + entityId + ', ' + attributeId);
                    io.emit('attribute.remove', {
                        entityId: entityId,
                        attributeId: attributeId
                    })
                },
                /**
                 * Update an EntityAttributeField's value
                 * @param entityId The ID of the entity to modify
                 * @param attributeId The ID of the EntityAttribute to modify
                 * @param fieldId The ID of the EntityAttributeField to modify
                 */
                update: function (entityId, attributeId, fieldId) {
                    n.info('Updating Attribute', 'Updating ' + $scope.entities[entityId].name + ' field to ' + $scope.form.attribute.edit[fieldId].value);
                    io.emit('attribute.update', {
                        entityId: entityId,
                        fieldId: fieldId,
                        value: $scope.form.attribute.edit[fieldId].value
                    });
                    $scope.form.attribute.edit[fieldId].expanded = false;
                    console.log('Update attribute: ' + entityId + ', ' + attributeId + ', ' + fieldId)
                }
            };
            //////////////////////////////////////////////////

            $scope.source = 'default';
            $scope.synicApi = {
                url: null,
                user: null,
                version: null,
                knowledgeGraphs: [],
                hasEEPipeline: false,
                connected: false
            };
            $scope.selectedKG = null;
            $scope.lastIngest = {
                ts: null,
                graphId: null,
                taskId: null
            };
            $scope.synic = {
                init: function () {
                    io.emit('synic.sync', null);
                    $scope.view = 'ingest';
                },
                sync: {
                    success: function (data) {
                        $scope.synicApi.version = data.api.version;
                        $scope.synicApi.url = data.url;
                        $scope.synicApi.user = data.user;
                        $scope.synicApi.connected = true;
                        $scope.synicApi.knowledgeGraphs = data.knowledge_graphs;
                        $scope.synicApi.hasEEPipeline = data.has_ee_pipeline;
                    }
                },
                ingest: {
                    submit: function () {
                        $scope.lastIngest.graphId = $scope.selectedKG;
                        io.emit('synic.ingest', {'kg': $scope.selectedKG})
                    },
                    success: function (data) {
                        n.success('Ingestion', 'Entities have been sent to Synthesys for ingestion with Task ID: '+ data.taskId);
                        $scope.lastIngest.taskId = data.taskId;
                        $scope.lastIngest.ts = moment();
                    }
                }
            };


            //////////////////////////////////////////////////

            io.on('attribute.sync', function (attributes) {
                $scope.attributes = attrSvc.sync(attributes);
            });

            io.on('entity.sync.all', function (entities) {
                $scope.entities = entitySvc.syncAll(entities);
            });

            io.on('entity.sync', function (entity) {
                $scope.entities[entity.id] = entitySvc.sync(entity);
            });

            io.on('entity.type.sync', function (types) {
                $scope.entityTypes = types;
            });

            io.on('entity.add.success', function () {
                $scope.entity.add.confirm();
                n.info('Add Entity', 'Entity added successfully.');
            });

            io.on('entity.add.failure', function () {
                $scope.entity.add.reattempt();
            });

            io.on('entity.export.all.success', function () {
                entitySvc.download();
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

            io.on('synic.sync', function (data) {
                $scope.synic.sync.success(data);
            });

            io.on('synic.ingest.success', function (data) {
                $scope.synic.ingest.success(data);
            });

            //////////////////////////////////////////////////

            io.emit('attribute.sync', null);
            io.emit('entity.sync.all', null);
            io.emit('entity.type.sync', null);
            io.emit('synic.sync', null);
        }])
});