<template>
  <v-container fluid>
    <!-- <button @click="checkNodes()">nodes</button> -->

    <!-- <v-btn @click="saveCanvas()">Save</v-btn>
    <v-btn @click="loadCanvas()">Load</v-btn> -->
    <v-toolbar elevation="1" dense>
      <v-btn class="mr-2" color="success" @click="saveCanvas">Save Modeling Draft</v-btn>
      <v-btn class="mr-2" color="accent" @click="loadModelCase">Load Modeling Draft</v-btn>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="secondary" @click="connectAllNodes" v-bind="attrs" v-on="on" class="mr-2">
            Connect All</v-btn
          >
        </template>
        <span>Connect Order (Input -> Algorithm -> Target)</span>
      </v-tooltip>

      <v-btn @click="runModel" color="primary"
        ><v-icon left small>mdi-play-outline</v-icon> Run</v-btn
      >

      <v-progress-circular
        v-show="progressBar == true"
        indeterminate
        color="primary"
      ></v-progress-circular>
    </v-toolbar>

    <!-- <v-btn @click="test()">test</v-btn> -->
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
import Display from "@/components/baklava/DisplayNode.js";
import Input from "@/components/baklava/feature/InputNode.js";
import Target from "@/components/baklava/feature/TargetNode.js";
// baklava option
import MyOption from "@/components/baklava/MyOption.vue";
import FeatureOption from "@/components/baklava/feature/FeatureOption.vue";
import FeatureSidebar from "@/components/baklava/feature/FeatureSidebar.vue";
import NormalizationSidebar from "@/components/baklava/feature/NormalizationSidebar.vue";
import AlgorithmOption from "@/components/baklava/algorithm/AlgorithmOption.vue";
import ParameterSidebar from "@/components/baklava/algorithm/ParameterSidebar.vue";

import axios from "axios";

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
      svr_parameters: ["kernel", "C", "epsilon", "gamma"],
      rf_parameters: ["n_estimators", "min_samples_split"],
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
      projectName: state => state.initialData.projectName,
      progressBar: state => state.modelingData.progressBar,
      modelingRequest: state => state.modelingData.modelingRequest,
      splitRatio: state => state.modelingData.splitRatio,
      columns: state => state.initialData.columns,
      canvasState: state => state.modelingData.canvasState
      // parameters: state => state.modelingData.parameters
    })
    // ...mapGetters("initialData", ["columns"]),
  },

  methods: {
    ...mapActions("modelingData", ["requestModeling"]),
    // mapmutations
    ...mapMutations("modelingData", ["saveModelingRequest"]),
    ...mapMutations("modelingData", ["showProgressBar"]),

    ...mapMutations("modelingData", ["saveGraphSources"]),
    ...mapMutations("modelingData", ["saveModelingSummary"]),
    ...mapMutations("modelingData", ["saveParameters"]),
    ...mapMutations("modelingData", ["saveCanvasState"]),
    ...mapMutations("modelingData", ["loadModelValue"]),

    ...mapActions("modelingData", ["saveModelCase"]),
    connectAllNodes() {
      let currentNodeCount = this.editor.nodes.length;
      if (currentNodeCount < 4) {
        alert("Algorithm Node가 컨버스상에 있어야 합니다.");
      } else {
        let Input = null;
        let algorithmNode = null;
        let Target = null;

        this.editor.nodes.forEach(element => {
          if (element.name == "Input") {
            Input = element;
          } else if (element.name == "Target") {
            Target = element;
          } else if (element.name == "Debugger") {
            return;
          } else {
            algorithmNode = element;
          }
        });
        this.editor.addConnection(Input.getInterface("Out"), algorithmNode.getInterface("In"));
        this.editor.addConnection(algorithmNode.getInterface("Out"), Target.getInterface("In"));
      }
    },
    async loadModelCase() {
      let path = "http://localhost:8000/loadModelCase";
      axios({
        method: "post",
        url: path,
        data: {
          caseName: "unnamed"
        }
      })
        .then(res => {
          this.loadModelValue(res.data);
          let result = this.editor.load(JSON.parse(this.canvasState));
          console.log(result);
        })
        .catch(error => {
          console.error(error);
        });
    },

    saveCanvas() {
      if (!confirm("현재 Modeling Process를 저장하시겠습니까?")) {
        return;
      } else {
        let state = JSON.stringify(this.editor.save());
        this.saveCanvasState(state);
        this.saveModelCase("unnamed");
      }
    },

    test() {
      console.log(this.editor.nodeTypes);
    },

    checkNodes() {
      this.calculate(this.engine);
    },
    async calculate(engine) {
      const result = await engine.calculate();
      this.algorithmRequest = null;
      for (const v of result.values()) {
        this.algorithmRequest = v;
      }
      let filteredInputs = this.algorithmRequest.inputs.filter(function(item) {
        return item != null || item != undefined;
      });
      let filteredTargets = this.algorithmRequest.targets.filter(function(item) {
        return item != null || item != undefined;
      });
      // Error Handling *Input - Target feature 중복 방지

      for (let i = 0; i < filteredInputs.length; i++) {
        if (filteredTargets.includes(filteredInputs[i])) {
          alert("Input과 Target에 중복되는 feature가 있습니다: " + filteredInputs[i]);
          return false;
        }
      }
      this.algorithmRequest.inputs = filteredInputs;
      this.algorithmRequest.targets = filteredTargets;
      this.saveModelingRequest(this.algorithmRequest);

      // 중복 없을 때만 vuex request
      // vuex request api, save response, and routing
    },

    // build node types
    // buildFeatureNodes(featureName) {
    //   let featureNode = new NodeBuilder("FeatureNode")
    //     .setName(featureName)
    //     .addOption("FeatureOption", "FeatureOption")
    //     .addOption(
    //       "Features",
    //       "ButtonOption",
    //       () => {
    //         return { features: "features" };
    //       },
    //       "FeatureSidebar"
    //     )
    //     .addOutputInterface("Out");

    //   // Input과 달리, Target의 경우 Input Interface도 필요하므로 추가
    //   if (featureName == "Target") {
    //     featureNode
    //       .addInputInterface("In")
    //       .addOption("ValueText", "TextOption")
    //       .onCalculate(n => {
    //         let result = n.getInterface("In").value;
    //         console.log(result);
    //         n.setOptionValue("ValueText", result);
    //       });
    //   }
    //   // console.log(featureNode.events);
    //   featureNode = featureNode.build();

    //   let category = "Features";
    //   this.editor.registerNodeType(featureName, featureNode, category);
    //   //Add Node
    //   let myNode = new featureNode();
    //   this.editor.addNode(myNode);

    //   if (featureName == "Input") {
    //     myNode.position = { x: 400, y: 300 };
    //   } else {
    //     myNode.position = { x: 1100, y: 300 };
    //   }
    // },

    async saveModelingDraft() {
      await this.calculate(this.engine); //vuex에 전송이 된 상태
      this.saveModelCase();
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
      const algorithmNode = new NodeBuilder(algorithmName)
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

        .addInputInterface("In")
        .addOutputInterface("Out")
        .onCalculate(n => {
          let nodeResult = n.getInterface("In").value;
          if (nodeResult != null) {
            let algorithmInfo = n.getOptionValue("Parameter");
            nodeResult["algorithm"] = algorithmInfo;
            n.getInterface("Out").value = nodeResult;
          }
        })
        .build();
      // this.node.getOptionValue("FeatureOption");
      let category = "Algorithm";

      this.editor.registerNodeType(algorithmName, algorithmNode, category);
    },
    async runModel() {
      this.showProgressBar(true);
      await this.calculate(this.engine);
      this.requestModeling();
    }
  },

  created() {
    eventBus.$on("closeSidebar", status => {
      this.viewPlugin.sidebar.visible = false;
    });
    eventBus.$on("loadModel", status => {
      this.loadModelCase();
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
    this.viewPlugin.registerOption("NormalizationSidebar", NormalizationSidebar);
    this.viewPlugin.registerOption("ParameterSidebar", ParameterSidebar);
    // // 2) register algorithm nodes

    this.algorithms.forEach(element => {
      this.buildAlgorithmNodes(element);
    });
    // Input
    let category = "Features";
    this.editor.registerNodeType("Input", Input, category);
    this.editor.registerNodeType("Target", Target, category);
    this.editor.registerNodeType("Display", Display, category);

    //Add Input Node
    let inputNode = new Input();
    this.editor.addNode(inputNode);
    inputNode.position = { x: 600, y: 330 };

    //Add Target Node
    let targetNode = new Target();
    this.editor.addNode(targetNode);
    // console.log(targetNode.interfaces);
    targetNode.position = { x: 1200, y: 330 };

    //Add Display Node
    let displayNode = new Display();
    this.editor.addNode(displayNode);
    displayNode.position = { x: 1400, y: 330 };

    this.editor.addConnection(
      this.editor.addConnection(targetNode.getInterface("Out"), displayNode.getInterface("In"))
    );
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
/* baklava custom css */
#baklavaStage {
  width: 100%;
  height: 100vh;
}
/* 배경 */
.node-editor .background {
  background-color: white !important;
  background-image: 
  /* 큰 네모 가로 세로 */ linear-gradient(
      rgb(228, 225, 225) 2px,
      transparent 2px
    ),
    linear-gradient(90deg, rgb(228, 225, 225) 2px, transparent 2px),
    /* 작은 네모 가로 세로*/ linear-gradient(rgb(228, 225, 225), transparent 1px),
    linear-gradient(90deg, rgb(228, 225, 225) 1px, transparent 1px) !important;
}
.node {
  background-color: rgb(255, 255, 255) !important;
  /* border: 1px solid; */
  color: black !important;
}
/* node 상단 */
.node .__title {
  /* background-color: rgb(67, 66, 66) !important; */
  background-color: #737373 !important;
}
.node .__title {
  text-align: center;
}
.node .__title span {
  font-weight: 600;
}
/* node 버튼/dropdown */
.node-option {
  /* background-color: rgb(169, 167, 167) !important; */
  font-weight: 500;
  background-color: rgb(223, 223, 223) !important;
  /* border: 0.5px solid rgb(70, 70, 70) !important; */
  /* color: rgba(0, 0, 0, 0.632) !important; */
  color: rgb(43, 42, 42) !important;
  /* border: 1px solid; */
}

/* node 선 */
.node-editor .connection {
  stroke: rgb(28, 28, 28);
}
.node-interface .__port {
  border: 1px solid rgba(0, 0, 0, 0.632);
}
.node_sidebar {
  background-color: #3f3f3f !important;
}
.__options button {
  margin-bottom: 5px;
}
</style>
