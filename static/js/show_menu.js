// Change delimiters not to conflict tornado.template delimiters.
Vue.config.delimiters = ['${', '}'];

var jsonPathDir = '/static/uploads/menu/';
var jsonPath = jsonPathDir + menuId + '.json';
var jqXHR = $.getJSON(jsonPath);

jqXHR.done(function(menuJson) {
  new Vue({
    el: '#app',
    data: menuJson,

    methods: {
      selectButton: function(index) {

        console.log('selectButton(' + (index + 1) + ')');

        robotBehavior = {
          'tabletAction': 'select_menu',
          'menuId': this.menuId,
          'selectionId': index + 1 // from 1 to len(selection)
        };

        window.parent.sendAction(robotBehavior);
      }
    }
  });
});
