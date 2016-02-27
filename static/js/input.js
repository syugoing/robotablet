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
  },
  methods: {
    selectButton: function(index) {
      sendAction(index);
      alert(index);
    }
  }
});

var show_menu_template = Vue.extend({
  template: '' +
'<div id="app">' +
'  <div class="row">' +
'    <div class="col m6 waves-effect waves-light" v-for="btn in btns">' +
'      <div class="card light-blue darken-1">' +
'        <div v-on:click="selectButton($index)" class="light-blue darken-1">' +
'          <div class="card-content">' +
'            <div class="btn-label-box-r2">' +
'              <h2 class="truncate left-align white-text btn-label">${ btn.label }</h2>' +
'            </div>' +
'          </div>' +
'        </div>' +
'      </div>' +
'    </div>' +
'  </div>' +
'</div>'
});

var show_image_template = Vue.extend({
  template: '<div>b A custom component!</div>'
});

new Vue({
  el: '#container',
  data: {
    currentView: 'show-image'
  },
  components: {
    'show-menu': show_menu_template,
    'show-image': show_image_template
  }
});
