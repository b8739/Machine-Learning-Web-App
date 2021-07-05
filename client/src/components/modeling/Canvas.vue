<template>
  <v-container fluid>
    <button @click="checkNodes()">nodes</button>
    <div id="baklavaStage">
      <baklava-editor :plugin="viewPlugin"></baklava-editor>
    </div>
  </v-container>
</template>
<script>
// baklavajs
import { Editor, NodeBuilder, Node, NodeOption } from "@baklavajs/core";
import { ViewPlugin } from "@baklavajs/plugin-renderer-vue";
import { OptionPlugin } from "@baklavajs/plugin-options-vue";
import CustomNode from "@/components/baklava/CustomNode.js";
// baklava option
import MyOption from "@/components/baklava/MyOption.vue";
import ParameterOption from "@/components/baklava/ParameterOption.vue";

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
      features: ["Input", "Target"],
      xgboost_props: [
        "n_estimators",
        "learning_rate",
        "gamma",
        "eta",
        "subsample",
        "colsample_bytree",
        "max_depth"
      ],
      editor: new Editor(),
      viewPlugin: new ViewPlugin(),
      node: new Node(),
      optionPlugin: new OptionPlugin(),
      options: {},
      algorithms: ["XGBoost", "SVR", "RF"],
      // props

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
    checkNodes() {
      console.log(this.editor.nodeTypes);
    },
    // mapmutations
    ...mapMutations("modelingResult", ["saveGraphSources"]),
    ...mapMutations("modelingResult", ["saveModelingSummary"]),
    ...mapMutations("modelingResult", ["saveParameters"]),

    // build node types
    buildFeatureNodes(featureName) {
      let newOption = new NodeOption();
      // 원래 하던거
      let featureNode = new NodeBuilder("FeatureNode")
        .setName(featureName)

        .addOption("MyOption", "MyOption")

        .addOutputInterface("Output")

        .onCalculate(n => {
          const n1 = n.getInterface("Number 1").value;
          const n2 = n.getInterface("Number 2").value;
          const operation = n.getOptionValue("Operation");
          let result;
          if (operation === "Add") {
            result = n1 + n2;
          } else if (operation === "Subtract") {
            result = n1 - n2;
          }
          n.getInterface("Output").value = result;
        });
      // Input과 달리, Target의 경우 Input Interface도 필요하므로 추가
      if (featureName == "Target") {
        featureNode.addInputInterface("Input");
      }
      // console.log(featureNode.events);
      featureNode = featureNode.build();

      let category = "Features";
      this.editor.registerNodeType(featureName, featureNode, category);
      //event
      let myNode = new featureNode();
      myNode.events.update.addListener(this, () => {
        console.log(this.node.getOptionValue("Operation"));
      });
    },
    buildAlgorithmNodes(algorithmName) {
      const algorithmNode = new NodeBuilder("AlgorithmNode")
        .setName(algorithmName)
        .addOption("Operation", "SelectOption", "Change Algorithm", undefined, {
          items: this.algorithms
        })
        .addOption("MyOption", "MyOption")
        .addOption(
          "Parameter",
          "ButtonOption",
          () => {
            return { parameters: this.xgboost_props };
          },
          "ParameterOption"
        )
        .addInputInterface("Input")
        .addOutputInterface("Output")
        .onCalculate(n => {
          const n1 = n.getInterface("Number 1").value;
          const n2 = n.getInterface("Number 2").value;
          const operation = n.getOptionValue("Operation");
          let result;
          if (operation === "Add") {
            result = n1 + n2;
          } else if (operation === "Subtract") {
            result = n1 - n2;
          }
          n.getInterface("Output").value = result;
        })
        .build();
      // this.node.getOptionValue("MyOption");
      let category = "Algorithm";
      this.editor.registerNodeType(algorithmName, algorithmNode, category);
    },
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
    }
  },
  created() {
    // baklava js setting
    this.editor.use(this.optionPlugin);
    this.editor.use(this.viewPlugin);

    // 1) viewPlugin option setting
    this.viewPlugin.registerOption("MyOption", MyOption);
    this.viewPlugin.registerOption("ParameterOption", ParameterOption);
    // 2) register algorithm nodes
    this.features.forEach(element => {
      this.buildFeatureNodes(element);
    });

    this.algorithms.forEach(element => {
      this.buildAlgorithmNodes(element);
    });
  },
  mounted() {}
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
