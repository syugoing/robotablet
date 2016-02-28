// Change delimiters not to conflict tornado.template delimiters.
Vue.config.delimiters = ['${', '}'];

new Vue({
  el: '#app',
  data: {
    menu_id: '101',
    btns: [{
      label: 'Ehime'
    }, {
      label: 'Kagawa'
    }, {
      label: 'Kochi'
    }, {
      label: 'Tokushima'
    }]
  },
  methods: {
    selectButton: function(index) {

      console.log('selectButton(' + (index + 1) + ')');

      robotBehavior = {
        'tabletAction': 'select_menu',
        'menuId': this.menu_id,
        'selectionId': index + 1 // from 1 to len(selection)
      };

      window.parent.sendAction(robotBehavior);
    }
  }
});
