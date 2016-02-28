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
      ws_contents = {
        'mode': 'stay_iframe',
        'menu_id': this.menu_id,
        'index': index
      };

      window.parent.sendAction(ws_contents);
    }
  }
});
