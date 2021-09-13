import axios from "axios";
import Vue from "vue";

const getDefaultState = () => {
  return {
    featureGraphData: null
  };
};
const state = getDefaultState();

const getters = {};

const mutations = {
  saveFeatureGraphData(state, payload) {
    state.featureGraphData = payload;
  }
};

const actions = {
  loadFeatureGraphData({ commit, state, rootState }) {
    let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/loadFeatureGraphData";
    // axios
    axios({
      method: "post",
      url: path,
      data: {
        tableName: rootState.initialData.tableName
      }
    })
      .then(res => {
        // console.log(res.data);
        // this.updateSeriesLine(res.data[this.seriesName], this.seriesName);
        commit("saveFeatureGraphData", res.data);
      })
      .catch(error => {
        console.error(error);
      });
    // dialog(edit modal)일때만 toolbar 활성화
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
