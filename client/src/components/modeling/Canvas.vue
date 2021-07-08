<template>
  <v-container fluid>
    <button @click="checkNodes()">nodes</button>

    <CanvasSide />

    <div id="baklavaStage" class="mt-1">
      <baklava-editor :plugin="viewPlugin"></baklava-editor>
    </div>
  </v-container>
</template>
<script>
// baklavajs
import { Editor, NodeBuilder, Node, NodeOption } from "@baklavajs/core";
import { Engine } from "@baklavajs/plugin-engine";
import { ViewPlugin } from "@baklavajs/plugin-renderer-vue";
import { OptionPlugin } from "@baklavajs/plugin-options-vue";
// nodes
import CustomNode from "@/components/baklava/CustomNode.js";
import DisplayNode from "@/components/baklava/DisplayNode.js";
import InputNode from "@/components/baklava/feature/InputNode.js";
import TargetNode from "@/components/baklava/feature/TargetNode.js";
// baklava option
import MyOption from "@/components/baklava/MyOption.vue";
import FeatureOption from "@/components/baklava/feature/FeatureOption.vue";
import FeatureSidebar from "@/components/baklava/feature/FeatureSidebar.vue";
import AlgorithmOption from "@/components/baklava/algorithm/AlgorithmOption.vue";
import ParameterSidebar from "@/components/baklava/algorithm/ParameterSidebar.vue";

import axios from "axios";
// drawflow
import Vue from "vue";
import Drawflow from "drawflow";
import styleDrawflow from "drawflow/dist/drawflow.min.css";
import NodeAlgorithm from "@/components/NodeAlgorithm.vue";
import CanvasSide from "@/components/modeling/CanvasSide.vue";

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
      algorithmRequest: null,
      engine: null,
      features: ["Input", "Target"],
      xgboost_parameters: [
        "n_estimators",
        "learning_rate",
        "gamma",
        "eta",
        "subsample",
        "colsample_bytree",
        "max_depth"
      ],
      svr_parameters: ["n_estimators", "min_samples_split"],
      rf_parameters: ["kernel", "C", "epsilon", "gamma"],
      // barklava
      editor: new Editor(),
      viewPlugin: new ViewPlugin(),
      node: new Node(),
      optionPlugin: new OptionPlugin(),
      algorithms: ["XGBoost", "SVR", "RF"],
      // props
      inputList: [],
      inputView: null
    };
  },
  components: { NodeAlgorithm, CanvasSide },
  computed: {
    ...mapState({
      inputs: state => state.modelingData.inputs,
      targets: state => state.modelingData.targets,
      algorithm: state => state.modelingData.algorithm
      // parameters: state => state.modelingData.parameters
    }),
    ...mapGetters("initialData", ["columns"]),
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
      this.calculate(this.engine);
    },
    async calculate(engine) {
      const result = await engine.calculate();
      console.log(result.values());
      for (const v of result.values()) {
        console.log(v);
      }
    },
    // mapmutations
    ...mapMutations("modelingResult", ["saveGraphSources"]),
    ...mapMutations("modelingResult", ["saveModelingSummary"]),
    ...mapMutations("modelingResult", ["saveParameters"]),

    // build node types
    buildFeatureNodes(featureName) {
      let featureNode = new NodeBuilder("FeatureNode")
        .setName(featureName)
        .addOption("FeatureOption", "FeatureOption")
        .addOption(
          "Features",
          "ButtonOption",
          () => {
            return { features: this.columns };
          },
          "FeatureSidebar"
        )
        .addOutputInterface("OUT");

      // Input과 달리, Target의 경우 Input Interface도 필요하므로 추가
      if (featureName == "Target") {
        featureNode
          .addInputInterface("IN")
          .addOption("ValueText", "TextOption")
          .onCalculate(n => {
            let result = n.getInterface("IN").value;
            console.log(result);
            n.setOptionValue("ValueText", result);
          });
      }
      // console.log(featureNode.events);
      featureNode = featureNode.build();

      let category = "Features";
      this.editor.registerNodeType(featureName, featureNode, category);
      //Add Node
      let myNode = new featureNode();
      this.editor.addNode(myNode);

      if (featureName == "Input") {
        myNode.position = { x: 400, y: 300 };
      } else {
        myNode.position = { x: 1100, y: 300 };
      }
    },
    buildAlgorithmNodes(algorithmName) {
      // dynamic parameter assign
      let parameters;
      if (algorithmName == "XGBoost") {
        parameters = this.xgboost_parameters;
      } else if (algorithmName == "SVR") {
        parameters = this.svr_parameters;
      } else {
        parameters = this.rf_parameters;
      }
      // Node type 생성
      const algorithmNode = new NodeBuilder("AlgorithmNode")
        .setName(algorithmName)
        .addOption("AlgorithmOption", "AlgorithmOption")
        .addOption(
          "Parameter",
          "ButtonOption",
          () => {
            return { parameterKeys: parameters };
          },
          "ParameterSidebar"
        )
        .addInputInterface("IN")
        .addOutputInterface("OUT")
        .onCalculate(n => {
          let nodeResult = n.getInterface("IN").value;
          if (nodeResult != null) {
            let algorithmInfo = n.getOptionValue("Parameter");
            nodeResult["algorithm"] = algorithmInfo;
            n.getInterface("OUT").value = nodeResult;
          }
        })
        .build();
      // this.node.getOptionValue("FeatureOption");
      let category = "Algorithm";
      this.editor.registerNodeType(algorithmName, algorithmNode, category);
      //Add Node
      // let myNode = new algorithmNode();
      // this.editor.addNode(myNode);
    },
    runModel() {
      this.algorithmRequest = this.calculate(this.engine);
      // eventBus.$emit("modelingParameter", modelingParameter);
      let path = "http://localhost:5000/xgboost_modeling";
      // define path
      if (this.algorithmRequest.algorithm.name == "XGBoost") {
        path += "xgboost_modeling";
      } else if (this.algorithm == "Random Forest") {
        path += "rf_modeling";
      } else if (this.algorithm == "SVR") {
        path += "svr_modeling";
      }
      // axios
      axios
        .get(path, {
          // params: {
          //   //algorithmProp 전송
          //   modelingParameter: modelingParameter
          // }
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
    // eventbus
    eventBus.$on("runModel", status => {
      this.runModel();
    });
    // baklava js setting
    this.editor.use(this.optionPlugin);
    this.editor.use(this.viewPlugin);
    this.engine = new Engine(true /* whether to automatically calculate on changes */);
    this.editor.use(this.engine);
    this.viewPlugin.enableMinimap = true;
    // 1) viewPlugin option setting
    this.viewPlugin.registerOption("MyOption", MyOption);
    this.viewPlugin.registerOption("FeatureOption", FeatureOption);
    this.viewPlugin.registerOption("AlgorithmOption", AlgorithmOption);
    this.viewPlugin.registerOption("FeatureSidebar", FeatureSidebar);
    this.viewPlugin.registerOption("ParameterSidebar", ParameterSidebar);
    // 2) register algorithm nodes

    this.algorithms.forEach(element => {
      this.buildAlgorithmNodes(element);
    });
    // InputNode
    let category = "Features";
    this.editor.registerNodeType("Input", InputNode, category);
    this.editor.registerNodeType("Target", TargetNode, category);

    //Add Input Node
    let inputNode = new InputNode();
    this.editor.addNode(inputNode);
    inputNode.position = { x: 600, y: 330 };

    //Add Target Node
    let targetNode = new TargetNode();
    this.editor.addNode(targetNode);
    // console.log(targetNode.interfaces);
    targetNode.position = { x: 1200, y: 330 };

    //Add Display Node
    let displayNode = new DisplayNode();
    this.editor.addNode(displayNode);
    displayNode.position = { x: 1400, y: 330 };

    this.editor.addConnection(
      this.editor.addConnection(targetNode.getInterface("OUT"), displayNode.getInterface("IN"))
    );

    // this.engine.events.calculated.addListener(this, result => {
    //   // result is a Map<Node, any> with the key being a node instance and the value being what the node's calculate function returned
    //   for (const v of result.values()) {
    //     console.log(v);
    //   }
    // });
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
