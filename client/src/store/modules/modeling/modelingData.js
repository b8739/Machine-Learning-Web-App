import axios from "axios";
import router from "@/router";

const state = {
  // request
  modelingRequest: null,
  splitRatio: null,
  // response from API
  graphSources: null,
  modelingSummary: null,
  caseList: [],
  caseDataset: null
};

const mutations = {
  // request
  saveModelingRequest(state, payload) {
    state.modelingRequest = payload;
  },
  saveSplitRatio(state, payload) {
    state.splitRatio = payload;
  },
  // response from API
  saveGraphSources(state, payload) {
    state.graphSources = payload;
  },
  saveModelingSummary(state, payload) {
    state.modelingSummary = payload;
  },
  saveCaseList(state, payload) {
    state.caseList = payload;
  },
  saveCaseDataset(state, payload) {
    state.caseDataset = payload;
  }
};

const actions = {
  requestModeling({ commit, state, rootState }) {
    // Error Validation (Check if Validation empty)
    for (const key in state.splitRatio) {
      if (state.splitRatio[key] == null || state.splitRatio[key].length == 0) {
        alert("Dataset Setting이 완료되지 않았습니다.");
        return false;
      }
    }
    //Error Validation (Check Test + Train ==100)
    if (parseInt(state.splitRatio["test"]) + parseInt(state.splitRatio["train"]) != 100) {
      alert("Test Set과 Train Set의 합이 100%가 아닙니다");
      return false;
    }
    // define path
    let algorithmName = state.modelingRequest["algorithm"]["name"].toLowerCase(); // xgboost/rf/svr
    let path = "http://localhost:5000/" + algorithmName + "_modeling";
    // let path = "http://localhost:5000/" + algorithmPath;
    console.log(path);
    console.log(state.modelingRequest);
    console.log(state.splitRatio);
    // axios
    axios({
      method: "post",
      url: path,
      data: {
        modelingRequest: state.modelingRequest,
        splitRatio: state.splitRatio,
        tableName: rootState.tableName
      }
    })
      .then(res => {
        commit("saveGraphSources", res.data[0]); // Test and Valid dataset
        commit("saveModelingSummary", res.data[1]); // Test and Valid dataset
        router.push({ path: "modelingResult/" + algorithmName });
      })
      .catch(error => {
        console.error(error);
      });
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
