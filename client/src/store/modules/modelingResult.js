const state = {
  graphSources: null,
  modelingSummary: null,
  caseList: [],
  caseInfo: null
};

const mutations = {
  saveGraphSources(state, payload) {
    state.graphSources = payload;
  },
  saveModelingSummary(state, payload) {
    state.modelingSummary = payload;
  },
  saveCaseList(state, payload) {
    state.caseList = payload;
  },
  saveCaseInfo(state, payload) {
    state.caseInfo = payload;
  }
};

const actions = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
