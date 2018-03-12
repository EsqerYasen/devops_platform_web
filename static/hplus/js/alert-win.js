(function($) {

    window.Alertwin = function() {
        var html = '<div id="[Id]" class="modal fade" role="dialog" aria-labelledby="modalLabel">' +
                        '<div class="modal-dialog modal-sm">' +
                            '<div class="modal-content">' +
                                '<div class="modal-header">' +
                                    '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button>' +
                                    '<h4 class="modal-title" id="modalLabel">[Title]</h4>' +
                                '</div>' +
                                '<div class="modal-body">' +
                                    '<p>[Message]</p>' +
                                '</div>' +
                                '<div class="modal-footer">' +
                                    '<button type="button" class="btn btn-primary ok" data-dismiss="modal">[BtnOk]</button>' +
                                    '<button type="button" class="btn btn-default cancel" data-dismiss="modal">[BtnCancel]</button>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>';

        var dialogdHtml = '<div id="[Id]" class="modal fade" role="dialog" aria-labelledby="modalLabel">' +
                              '<div class="modal-dialog">' +
                                  '<div class="modal-content">' +
                                      '<div class="modal-header">' +
                                          '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button>' +
                                          '<h4 class="modal-title" id="modalLabel">[Title]</h4>' +
                                      '</div>' +
                                      '<div class="modal-body">' +
                                      '</div>' +
                                  '</div>' +
                              '</div>' +
                          '</div>';

        var alertHtml = '<div id="[Id]" class="modal fade" role="dialog" aria-labelledby="modalLabel">' +
                        '<div class="modal-dialog modal-sm">' +
                            '<div class="modal-content">' +
                                '<div class="modal-header">' +
                                    '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button>' +
                                    '<h4 class="modal-title" id="modalLabel">[Title]</h4>' +
                                '</div>' +
                                '<div class="modal-body">' +
                                    '<p>[Message]</p>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>';

        var openWinHtml = '<div id="[Id]" class="modal fade" role="dialog" aria-labelledby="modalLabel">' +
                      '<div class="modal-dialog">' +
                          '<div class="modal-content" style="width:[Width]px;height:[Height]px">' +
                              '<div class="modal-header" style="height:60px">' +
                                  '<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">×</span><span class="sr-only">Close</span></button>' +
                                  '<h4 class="modal-title" id="modalLabel">[Title]</h4>' +
                              '</div>' +
                              '<div class="modal-body" style="height:[MbHeight]px">' + //
                              '</div>' +
                              '<div class="modal-footer" style="height:60px;">' +
                                '<button type="button" style="display:[BtnOkDisplay]" class="btn btn-primary ok" data-dismiss="modal">[BtnOk]</button>' +
                                '<button type="button" style="display:[BtnCancelDisplay]" class="btn btn-default cancel" data-dismiss="modal">[BtnCancel]</button>' +
                              '</div>' +
                          '</div>' +
                      '</div>' +
                  '</div>';

        var reg = new RegExp("\\[([^\\[\\]]*?)\\]", 'igm');
        var generateId = function() {
            var date = new Date();
            return 'mdl' + date.valueOf();
        }
        var init = function(options) {
            options = $.extend({},
            {
                title: "操作提示",
                message: "提示内容",
                btnok: "确定",
                btncl: "取消",
                width: 300,
                auto: false
            },
            options || {});
            var modalId = generateId();
            var content = html.replace(reg,
            function(node, key) {
                return {
                    Id: modalId,
                    Title: options.title,
                    Message: options.message,
                    BtnOk: options.btnok,
                    BtnCancel: options.btncl
                } [key];
            });
            $('body').append(content);
            $('#' + modalId).modal({
                width: options.width,
                backdrop: 'static'
            });
            $('#' + modalId).on('hide.bs.modal',
            function(e) {
                $('body').find('#' + modalId).remove();
            });
            return modalId;
        }

        return {
            alert: function(options) {
                if (typeof options == 'string') {
                    options = {
                        message: options
                    };
                }
                var id = init(options);
                var modal = $('#' + id);
                modal.find('.ok').removeClass('btn-success').addClass('btn-primary');
                modal.find('.cancel').hide();

                return {
                    id: id,
                    on: function(callback) {
                        if (callback && callback instanceof Function) {
                            modal.find('.ok').click(function() {
                                callback(true);
                            });
                        }
                    },
                    hide: function(callback) {
                        if (callback && callback instanceof Function) {
                            modal.on('hide.bs.modal',
                            function(e) {
                                callback(e);
                            });
                        }
                    }
                };
            },
            confirm: function(options) {
                var id = init(options);
                var modal = $('#' + id);
                modal.find('.ok').removeClass('btn-primary').addClass('btn-success');
                modal.find('.cancel').show();
                return {
                    id: id,
                    on: function(callback) {
                        if (callback && callback instanceof Function) {
                            modal.find('.ok').click(function() {
                                callback(true);
                            });
                            modal.find('.cancel').click(function() {
                                callback(false);
                            });
                        }
                    },
                    hide: function(callback) {
                        if (callback && callback instanceof Function) {
                            modal.on('hide.bs.modal',
                            function(e) {
                                callback(e);
                            });
                        }
                    }
                };
            },
            dialog: function(options) {
                options = $.extend({},
                {
                    title: 'title',
                    url: '',
                    width: 800,
                    height: 550,
                    onReady: function() {},
                    onShown: function(e) {}
                },
                options || {});
                var modalId = generateId();

                var content = dialogdHtml.replace(reg,
                function(node, key) {
                    return {
                        Id: modalId,
                        Title: options.title
                    } [key];
                });
                $('body').append(content);
                var target = $('#' + modalId);
                target.find('.modal-body').load(options.url);
                if (options.onReady()) options.onReady.call(target);
                target.modal();
                target.on('shown.bs.modal',
                function(e) {
                    if (options.onReady(e)) options.onReady.call(target, e);
                });
                target.on('hide.bs.modal',
                function(e) {
                    $('body').find(target).remove();
                });
            },
            openwin: function(options) {
                options = $.extend({},
                {
                    title: 'title',
                    content: '',
                    width: 600,
                    height: 450,
                    btnok: "确定",
                    btncl: "取消",
                    BtnOkDisplay:'inline-block',
                    BtnCancelDisplay:'inline-block',
                    onReady: function() {},
                    onShown: function(e) {}
                },
                options || {});

                var modalId = generateId();

                var content = openWinHtml.replace(reg,
                function(node, key) {
                    return {
                        Id: modalId,
                        Title: options.title,
                        Height:options.height,
                        Width:options.width,
                        MbHeight:options.height-120,
                        BtnOk: options.btnok,
                        BtnCancel: options.btncl,
                        BtnOkDisplay:options.BtnOkDisplay,
                        BtnCancelDisplay:options.BtnCancelDisplay
                    } [key];
                });
                $('body').append(content);

                var modal = $('#' + modalId);
                modal.find('.ok').removeClass('btn-primary').addClass('btn-success');
                modal.find('.cancel').show();
                modal.find('.modal-body').append(options.content);
                if (options.onReady()) options.onReady.call(modal);
                modal.modal();
                modal.on('shown.bs.modal',
                function(e) {
                    if (options.onReady(e)) options.onReady.call(modal, e);
                });
                modal.on('hide.bs.modal',
                function(e) {
                    $('body').find(modal).remove();
                });
                return {
                    id: modalId,
                    on: function(callback) {
                        if (callback && callback instanceof Function) {
                            modal.find('.ok').click(function() {
                                callback(true);
                            });
                            modal.find('.cancel').click(function() {
                                callback(false);
                            });
                        }
                    },
                    hide: function(callback) {
                        if (callback && callback instanceof Function) {
                            modal.on('hide.bs.modal',
                            function(e) {
                                callback(e);
                            });
                        }
                    }
                };

            }
        }
    } ();
})(jQuery);


function showPopover(target, msg) {
  target.attr("data-original-title", msg);
  $('[data-toggle="tooltip"]').tooltip();
  target.tooltip('show');
  target.focus();
  var id = setTimeout(
    function () {
      target.attr("data-original-title", "");
      target.tooltip('hide');
    }, 3000
  );
}