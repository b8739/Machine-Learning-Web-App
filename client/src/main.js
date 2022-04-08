import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "@/store/index";
// global component
import Header from "@/components/preprocess/Header.vue";
Vue.component("Header", Header);
// axios
import axios from "axios";
Vue.prototype.$axios = axios;

// apex charts
// import VueApexCharts from "vue-apexcharts";
// portal
import PortalVue from "portal-vue";

// vuetify
// import Vuetify from "vuetify";
import vuetify from "@/plugins/vuetify"; // path to vuetify export
// export default new Vuetify({});
// Vue.use(Vuetify);
// import "vuetify/dist/vuetify.min.css";

// BaklavaVuePlugin
import { BaklavaVuePlugin, PluginOptionsVue } from "@baklavajs/plugin-renderer-vue";
import { OptionPlugin } from "@baklavajs/plugin-options-vue";

import "@baklavajs/plugin-renderer-vue/dist/styles.css";
Vue.use(BaklavaVuePlugin);

//fort-awesome
import { library } from "@fortawesome/fontawesome-svg-core";
import { faChartLine } from "@fortawesome/free-solid-svg-icons";
import { faChartArea } from "@fortawesome/free-solid-svg-icons";
import { faChartBar } from "@fortawesome/free-solid-svg-icons";
import { faChartPie } from "@fortawesome/free-solid-svg-icons";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(faChartLine);
library.add(faTrash);
library.add(faChartArea);
library.add(faChartBar);
library.add(faChartPie);

// fontawesome
Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.config.productionTip = false;

Vue.use(PortalVue);

//vue modal js

import VModal from "vue-js-modal";
Vue.use(VModal);
// Vue.component("apexchart", VueApexCharts);
Vue.config.productionTip = false;

export const eventBus = new Vue();

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
