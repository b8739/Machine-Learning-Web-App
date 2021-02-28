import BootstrapVue from 'bootstrap-vue';
// import Vuetify from 'vuetify';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import VueApexCharts from 'vue-apexcharts'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css'

// import 'vuetify/dist/vuetify.min.css';

// Vue.use(Vuetify);

Vue.use(BootstrapVue);
Vue.component('apexchart', VueApexCharts)
Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
