import axios from "axios";
import router from "@/router";
import Vue from "vue";

const getDefaultState = () => {
  return {
    // request
    modelingRequest: { inputs: null, targets: null, algorithm: { parameters: null, name: null } }, //from Canvas.vue (calculation)

    modelingDataset: null,
    splitRatio: {
      // from CanvasSide.vue (computed v-model)
      test: null,
      train: null,
      validation: null
    },
    graphSources: {},
    modelingSummary: {},

    selectedGrid: null,
    // response from API

    caseList: [],
    caseDataset: null,
    parameterKeys: null,
    progressBar: false,
    modelSaveDialog: false,
    canvasState: null
  };
};
const state = getDefaultState();

const mutations = {
  loadModelValue(state, payload) {
    Vue.set(state.modelingRequest, "inputs", payload.inputs);
    Vue.set(state.modelingRequest, "targets", payload.targets);

    Vue.set(state.modelingRequest.algorithm, "parameters", payload.parameters);
    Vue.set(state.modelingRequest.algorithm, "name", payload.algorithm);

    state.modelingDataset = payload.modelingDataset;

    state.canvasState = payload.canvasState;

    Vue.set(state.splitRatio, "test", payload.splitRatio.test);
    Vue.set(state.splitRatio, "train", payload.splitRatio.train);
    Vue.set(state.splitRatio, "validation", payload.splitRatio.validation);
  },
  saveCanvasState(state, payload) {
    state.canvasState = payload;
  },
  setRatioValue(state, payload) {
    console.log(payload);
    state.splitRatio[payload.target] = payload.value;
  },
  showProgressBar(state, payload) {
    state.progressBar = payload;
  },
  showModelSaveDialog(state, payload) {
    state.modelSaveDialog = payload;
  },
  setParameterKeys(state, payload) {
    state.parameterKeys = payload;
  },
  setSelectedGrid(state, payload) {
    state.selectedGrid = payload;
  },
  // request
  saveModelingRequest(state, payload) {
    state.modelingRequest = payload;
  },
  saveDatasetInfo(state, payload) {
    state.modelingDataset = payload;
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
  },
  resetModelingData(state) {
    Object.assign(state, getDefaultState());
  },
  removeUndefined(state, arrayName) {
    state.modelingRequest[arrayName].filter((element, i) => element !== undefined);
  }
};

const actions = {
  loadCases() {
    let path = "http://localhost:8000/loadCases";
    axios
      .get(path)
      .then(res => {
        commit("saveCaseList", res.data);
      })
      .catch(error => {});
  },
  saveModelCase({ commit, state, rootState, dispatch }, case_name) {
    let path = "http://localhost:8000/saveModelCase";
    axios({
      method: "post",
      url: path,
      data: {
        projectName: rootState.initialData.projectName,
        modelingDataset: state.modelingDataset,
        splitRatio: state.splitRatio,

        case_name: case_name,

        inputs: state.modelingRequest.inputs,
        targets: state.modelingRequest.targets,
        parameters: state.modelingRequest.algorithm.parameters,
        algorithm: state.modelingRequest.algorithm.name,

        modelingSummary: state.modelingSummary,
        graphSources: state.graphSources,
        canvasState: state.canvasState
      }
    }).then(function(res) {
      alert(res.data);
      dispatch("loadCases");
    });

    commit("showModelSaveDialog", false);
  },
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
    let path = "http://localhost:8000/modeling/" + algorithmName;
    // let path = "http://localhost:8000/" + algorithmPath;
    console.log(path);
    console.log(state.modelingRequest);
    console.log(state.splitRatio);
    commit("removeUndefined", "inputs");
    commit("removeUndefined", "targets");
    // axios
    axios({
      method: "post",
      url: path,
      data: {
        projectName: rootState.initialData.projectName,
        modelingRequest: state.modelingRequest,
        modelingDataset: state.modelingDataset, // 어떤 draft, 어떤 grid인지 보내주고 나머지는 () mongodb에서 가져오면됨
        splitRatio: state.splitRatio
      }
    })
      .then(res => {
        commit("saveGraphSources", res.data[0]); // Test and Valid dataset
        commit("saveModelingSummary", res.data[1]); // Test and Valid dataset
        router.push({ path: "/modelingResult/" + algorithmName });
      })
      .catch(error => {
        alert(error.response.data);
      })
      .finally(() => {
        commit("showProgressBar", false);
      });
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
