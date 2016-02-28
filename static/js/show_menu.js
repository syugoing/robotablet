// Change delimiters not to conflict tornado.template delimiters.
Vue.config.delimiters = ['${', '}'];

new Vue({
  el: '#app',
  data: {
    menu_id: 101,
    btns: [{
      label: '①　愛媛県'
    }, {
      label: '②　香川県'
    }, {
      label: '③　高知県'
    }, {
      label: '④　徳島県'
    }]
  },
  methods: {
    selectButton: function(index) {
      contents = {'mode': 'stay_iframe', 'menu_id': this.menu_id, 'index': index};
      window.parent.sendAction(contents);
    }
  }
});
