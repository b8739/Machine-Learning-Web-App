import axios from "axios";
import Vue from "vue";

const state = {
  apexChartDataset: {}
};

const getters = {};

const mutations = {
  setApexChartDataset(state, payload) {
    Vue.set(state.apexChartDataset, payload.featureName, payload.dataset);
    // state.apexChartDataset[payload.featureName] = payload.dataset;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
