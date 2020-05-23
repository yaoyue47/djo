 $(document).ready(function() {

            var widget = $('.tabs-basic');

            var tabs = widget.find('ul a'),
                content = widget.find('.tabs > div');

            tabs.on('click', function (e) {

                e.preventDefault();               

                var index = $(this).data('index');

                tabs.removeClass('tab-active');
                content.removeClass('tabs-active');
                content.addClass("tabs-disactive");

                $(this).addClass('tab-active');
                 content.eq(index).removeClass('tabs-disactive');
                content.eq(index).addClass('tabs-active');

            });

        });