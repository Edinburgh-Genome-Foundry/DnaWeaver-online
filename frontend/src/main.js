// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App'
import VTooltip from 'v-tooltip'
import widgets from './components/widgets'
import VueResource from 'vue-resource'

import './fontawesome-icons'

Vue.use(ElementUI)
Vue.use(VTooltip)
Vue.use(widgets)
Vue.use(VueResource)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
