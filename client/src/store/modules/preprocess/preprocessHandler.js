import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    preprocessStatus: null,
    editMode: false,
    editStatus: { "table-insert-row": false, "summary-change-name": false }
  };
};
const state = getDefaultState();

const getters = {};

const mutations = {
  setPreprocessStatus(state, payload) {
    state.preprocessStatus = payload;
  },
  setEditMode(state, payload) {
    state.editMode = payload;
  },
  setEditStatus(state, payload) {
    state.editStatus[state.preprocessStatus] = payload;
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
