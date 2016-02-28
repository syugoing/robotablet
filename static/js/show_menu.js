// Change delimiters not to conflict tornado.template delimiters.
Vue.config.delimiters = ['${', '}'];

new Vue({
  el: '#app',
  data: {
    menu_id: 101,
    btns: [{
      label: '1. Ehime'
    }, {
      label: '2. Kagawa'
    }, {
      label: '3. Kochi'
    }, {
      label: '4. Tokushima'
    }]
  },
  methods: {
    selectButton: function(index) {

      console.log('selectButton(' + index + ')');

      robotBehavior = {
        'tablet_action': 'select_menu',
        'menu_id': this.menu_id,
        'selection_id': index + 1 // from 1 to len(selection)
      };

      window.parent.sendAction(robotBehavior);
    }
  }
});
