/*globals define, _, WebGMEGlobal*/
/**
 * Generated by VisualizerGenerator 1.7.0 from webgme on Fri Apr 23 2021 18:59:49 GMT-0400 (Eastern Daylight Time).
 */

define([
    'js/PanelBase/PanelBaseWithHeader',
    'js/PanelManager/IActivePanel',
    'widgets/PetrinetView/PetrinetViewWidget',
    './PetrinetViewControl'
], function (
    PanelBaseWithHeader,
    IActivePanel,
    PetrinetViewWidget,
    PetrinetViewControl
) {
    'use strict';

    function PetrinetViewPanel(layoutManager, params) {
        var options = {};
        //set properties from options
        options[PanelBaseWithHeader.OPTIONS.LOGGER_INSTANCE_NAME] = 'PetrinetViewPanel';
        options[PanelBaseWithHeader.OPTIONS.FLOATING_TITLE] = true;

        //call parent's constructor
        PanelBaseWithHeader.apply(this, [options, layoutManager]);

        this._client = params.client;

        //initialize UI
        this._initialize();

        this.logger.debug('ctor finished');
    }

    //inherit from PanelBaseWithHeader
    _.extend(PetrinetViewPanel.prototype, PanelBaseWithHeader.prototype);
    _.extend(PetrinetViewPanel.prototype, IActivePanel.prototype);

    PetrinetViewPanel.prototype._initialize = function () {
        var self = this;

        //set Widget title
        this.setTitle('');

        this.widget = new PetrinetViewWidget(this.logger, this.$el);

        this.widget.setTitle = function (title) {
            self.setTitle(title);
        };

        this.control = new PetrinetViewControl({
            logger: this.logger,
            client: this._client,
            widget: this.widget
        });

        this.onActivate();
    };

    /* OVERRIDE FROM WIDGET-WITH-HEADER */
    /* METHOD CALLED WHEN THE WIDGET'S READ-ONLY PROPERTY CHANGES */
    PetrinetViewPanel.prototype.onReadOnlyChanged = function (isReadOnly) {
        //apply parent's onReadOnlyChanged
        PanelBaseWithHeader.prototype.onReadOnlyChanged.call(this, isReadOnly);

    };

    PetrinetViewPanel.prototype.onResize = function (width, height) {
        this.logger.debug('onResize --> width: ' + width + ', height: ' + height);
        this.widget.onWidgetContainerResize(width, height);
    };

    /* * * * * * * * Visualizer life cycle callbacks * * * * * * * */
    PetrinetViewPanel.prototype.destroy = function () {
        this.control.destroy();
        this.widget.destroy();

        PanelBaseWithHeader.prototype.destroy.call(this);
        WebGMEGlobal.KeyboardManager.setListener(undefined);
        WebGMEGlobal.Toolbar.refresh();
    };

    PetrinetViewPanel.prototype.onActivate = function () {
        this.widget.onActivate();
        this.control.onActivate();
        WebGMEGlobal.KeyboardManager.setListener(this.widget);
        WebGMEGlobal.Toolbar.refresh();
    };

    PetrinetViewPanel.prototype.onDeactivate = function () {
        this.widget.onDeactivate();
        this.control.onDeactivate();
        WebGMEGlobal.KeyboardManager.setListener(undefined);
        WebGMEGlobal.Toolbar.refresh();
    };

    return PetrinetViewPanel;
});
