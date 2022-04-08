import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    //   x
    xaxisColumns: [null],
    xaxisEvent: null,
    // y

    yaxisColumns: [null],
    yaxisEvent: null
  };
};
const state = getDefaultState();

const getters = {};

const mutations = {
  // x
  setXaxisColumn(state, payload) {
    state.xaxisColumns = payload;
  },

  removeXaxisColumn(state, payload) {
    let idx = state.xaxisColumns.indexOf(payload);
    Vue.delete(state.xaxisColumns, idx);
  },

  setXaxisEvent(state, payload) {
    state.xaxisEvent = payload;
  },
  //   y
  setYaxisColumn(state, payload) {
    state.yaxisColumns = payload;
  },

  removeYaxisColumn(state, payload) {
    let idx = state.yaxisColumns.indexOf(payload);
    Vue.delete(state.yaxisColumns, idx);
  },

  setYaxisEvent(state, payload) {
    state.yaxisEvent = payload;
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
