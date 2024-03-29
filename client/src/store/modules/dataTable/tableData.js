import Vue from "vue";

const getDefaultState = () => {
  return {
    activatedEvent: null
  };
};
const state = getDefaultState();

const getters = {};

const mutations = {};
const actions = {
  activateDeleteRow({ commit, state, rootState }, payload) {
    commit("activateEditMode", true);
    state.activatedEvent = () => {
      let numOfRows = payload.length;
      payload.forEach(element => {
        console.log(element);
        Vue.delete(state.datasetItems, element);
      });
      alert(`Total ${numOfRows} row(s) Successfully Deleted!`); //삭제 알림
      rootState.initialData.setDatasetSize(rootState.initialData.datasetSize - numOfRows);
      commit("activateEditMode", false);
    };
  }
};
export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
