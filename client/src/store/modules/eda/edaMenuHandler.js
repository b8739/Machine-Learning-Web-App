import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    menuState: "data"
  };
};
const state = getDefaultState();

const getters = {};

const mutations = {
  setMenuState(state, payload) {
    state.menuState = payload;
  },
  resetEda(state) {
    Object.assign(state, getDefaultState());
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
