import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    preprocessStatus: null,
    editMode: false,
    editStatus: {
      tableInsertRow: false,
      summaryChangeName: false,
      summaryChangeType: false,
      summaryChangeOrderModal: false
    },
    activatedEvent: null,
    additionalCancelEvent: null
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
  setAllEditStatus(state, payload) {
    Object.keys(state.editStatus).forEach(element => {
      Vue.set(state.editStatus, element, payload);
    });
  },
  setEditStatus(state, payload) {
    state.editStatus[state.preprocessStatus] = payload;
  },

  setEvent(state, payload) {
    state.activatedEvent = payload;
  },
  setAdditionalCancelEvent(state, payload) {
    state.additionalCancelEvent = payload;
  },
  resetPreprocessVuex(state) {
    Object.assign(state, getDefaultState());
  }
};

const actions = {
  cancelEvent({ commit, state }) {
    commit("setAllEditStatus", false);
    commit("setPreprocessStatus", null);
    commit("setEditMode", false);
    commit("setEvent", null);

    if (state.additionalCancelEvent != null) return state.additionalCancelEvent();
  },
  activateEvent({ commit, state }, payload) {
    commit("setPreprocessStatus", payload);
    commit("setEditStatus", true);
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
