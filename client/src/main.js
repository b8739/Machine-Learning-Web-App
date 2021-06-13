import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "@/store/index";
// global component
import Header from "@/components/layout/Header.vue";
Vue.component("Header", Header);
// axios
import axios from "axios";
Vue.prototype.$axios = axios;

// konva
import VueKonva from "vue-konva";
// apex charts
import VueApexCharts from "vue-apexcharts";
// portal
import PortalVue from "portal-vue";
// bootstrap
import BootstrapVue from "bootstrap-vue";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
// vuetify
import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";

//fort-awesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { faChartLine } from "@fortawesome/free-solid-svg-icons";
import { faChartArea } from "@fortawesome/free-solid-svg-icons";
import { faChartBar } from "@fortawesome/free-solid-svg-icons";
import { faChartPie } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import "..//node_modules/jointjs/css/layout.css";

library.add(faChartLine);
library.add(faChartArea);
library.add(faChartBar);
library.add(faChartPie);

Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.config.productionTip = false;

Vue.use(PortalVue);
Vue.use(Vuetify);

Vue.use(VueKonva);
// Vue.use(Vuetify);

Vue.use(BootstrapVue);
Vue.component("apexchart", VueApexCharts);
Vue.config.productionTip = false;

// jointjs;
window.$ = require("jquery");
window.joint = require("jointjs");

export const eventBus = new Vue();

new Vue({
  router,
  store,

  vuetify: new Vuetify(),
  render: h => h(App)
}).$mount("#app");
