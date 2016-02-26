// Change delimiters not to conflict tornado.template delimiters.
Vue.config.delimiters = ['${', '}'];

new Vue({
  el: '#app',
  data: {
    btns: [{
      label: '①　愛媛県'
    }, {
      label: '②　香川県'
    }, {
      label: '③　高知県'
    }, {
      label: '④　徳島県'
    }]
  }
});
