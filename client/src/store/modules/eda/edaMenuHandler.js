import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    menuState: "traces"
  };
};
const state = getDefaultState();

const getters = {};

const mutations = {
  setMenuState(state, payload) {
    state.menuState = payload;
  }
};

const actions = {
  //   loadFeatureGraphData({ commit, state, rootState }) {
  //   }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
