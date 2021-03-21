import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store'
// apex charts
import VueApexCharts from 'vue-apexcharts'
// portal
import PortalVue from 'portal-vue'
// bootstrap
import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css'
// vuetify
// import Vuetify from 'vuetify';
// import 'vuetify/dist/vuetify.min.css';


Vue.use(PortalVue)


// Vue.use(Vuetify);

Vue.use(BootstrapVue);
Vue.component('apexchart', VueApexCharts)
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
