<template>
  <v-container>
    <div id="baklavaStage">
      <baklava-editor :plugin="viewPlugin"></baklava-editor>
    </div>
  </v-container>
</template>
<script>
// baklavajs
import { Editor } from "@baklavajs/core";
import { ViewPlugin } from "@baklavajs/plugin-renderer-vue";
import customNode from "@/components/customNode.js";

import axios from "axios";
// drawflow
import Vue from "vue";
import Drawflow from "drawflow";
import styleDrawflow from "drawflow/dist/drawflow.min.css";
import NodeAlgorithm from "@/components/NodeAlgorithm.vue";

axios.defaults.paramsSerializer = function(paramObj) {
  const params = new URLSearchParams();
  for (const key in paramObj) {
    params.append(key, paramObj[key]);
  }

  return params.toString();
};

import { eventBus } from "@/main";
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      editor: new Editor(),
      viewPlugin: new ViewPlugin(),

      options: {},

      // props
      xgboost_props: [
        "n_estimators",
        "learning_rate",
        "gamma",
        "eta",
        "subsample",
        "colsample_bytree",
        "max_depth"
      ],
      svr_props: ["kernel", "C", "epsilon", "gamma"],
      randomForest_props: ["n_estimators", "min_samples_split"],
      // options
      selectedProps: [500, 0.08, 0.3, 0.04, 0.75, 0.5, 7],
      xTrain: [
        "CRIM",
        "ZN",
        "INDUS",
        "CHAS",
        "NOX",
        "RM",
        "AGE",
        "DIS",
        "RAD",
        "TAX",
        "PTRATIO",
        "B",
        "LSTAT"
      ],
      yTrain: ["MEDV"],
      inputList: [],
      inputView: null
    };
  },
  components: { NodeAlgorithm },
  computed: {
    ...mapState({
      inputs: state => state.modelingData.inputs,
      targets: state => state.modelingData.targets,
      algorithm: state => state.modelingData.algorithm,
      parameters: state => state.modelingData.parameters
    }),
    ...mapGetters({
      columns: state => state.initialData.columns
    }),
    algorithmProps() {
      if (this.algorithm == "XGBoost") {
        return this.xgboost_props;
      } else if (this.algorithm == "Random Forest") {
        return this.randomForest_props;
      } else if (this.algorithm == "SVR") {
        return this.svr_props;
      }
    }
  },

  methods: {
    ...mapMutations("modelingResult", ["saveGraphSources"]),
    ...mapMutations("modelingResult", ["saveModelingSummary"]),
    ...mapMutations("modelingResult", ["saveParameters"]),

    runModel(modelingParameter) {
      eventBus.$emit("modelingParameter", modelingParameter);
      let path = "http://localhost:5000/";
      // define path
      if (this.algorithm == "XGBoost") {
        path += "xgboost_modeling";
      } else if (this.algorithm == "Random Forest") {
        path += "rf_modeling";
      } else if (this.algorithm == "SVR") {
        path += "svr_modeling";
      }
      // axios
      axios
        .get(path, {
          params: {
            //algorithmProp 전송
            modelingParameter: modelingParameter
          }
        })
        .then(res => {
          // vuex
          this.saveGraphSources(res.data[0]); // Test and Valid dataset
          this.saveModelingSummary(res.data[1]); //modeling summary (ex.MAPE)
          //canvas 감추기

          this.$router.push({ name: "modelingResult" });
        })
        .catch(error => {
          console.error(error);
        });
    },
    createNode(nodeInfo) {
      // parameter ready
      let hasParameter = null;
      if (nodeInfo.nodeType == "algorithm") {
        hasParameter = true;
      } else {
        hasParameter = false;
      }
      const props = { name: nodeInfo.node, hasParameter: hasParameter };
      const options = {};
      const data = {};
      // register
      this.editor.registerNode("Block", NodeAlgorithm, props, options);
      this.editor.addNode("Name", 1, 1, 200, 100, "Class", data, "Block", "vue");
    }
  },
  created() {
    this.editor.use(this.optionPlugin);
    this.editor.use(this.viewPlugin);

    // register your nodes, node options, node interface types, ...

    this.editor.registerNodeType("customNode", customNode);
    eventBus.$on("runModel", status => {
      this.runModel(this.selectedProps);
      this.saveParameters(this.selectedProps);
    });
    eventBus.$on("sendNodeInfo", nodeInfo => {
      this.createNode(nodeInfo);
    });
  },
  mounted() {
    // drawflow
    const id = document.getElementById("drawflow");
    // editor
    this.editor = new Drawflow(id, Vue);
    this.editor.start();
    const props = { name: "Input" };

    // register
    this.editor.registerNode("NodeAlgorithm1", NodeAlgorithm, props, this.options);

    const data = {};
    this.editor.addNode("Name", 1, 1, 200, 100, "Class", data, "NodeAlgorithm1", "vue");
    this.editor.addNode("Name", 1, 1, 300, 500, "Class", data, "NodeAlgorithm1", "vue");
  }
};
</script>
<style>
#stage {
  width: 1000px;
  height: 1000px;
}
.columnList {
  height: 400px;
  overflow-y: scroll;
}
/* drawflow */
#drawflow {
  width: 100%;
  height: 100vh;
}
#baklavaStage {
  width: 100%;
  height: 100vh;
}
</style>
