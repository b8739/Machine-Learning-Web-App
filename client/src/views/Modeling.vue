<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2">
        <ModelingSide v-if="modelingProcess" />
        <ModelingResultSide v-else />
      </v-col>
      <v-col cols="10">
        <v-toolbar elevation="1" dense>
          <v-spacer></v-spacer
          ><v-btn @click="runModel" v-if="modelingProcess"
            ><v-icon left small>mdi-play-outline</v-icon> Run</v-btn
          >
          <v-btn v-else @click="dialog = true">Save Model</v-btn>
        </v-toolbar>
        <Canvas v-if="showCanvas"></Canvas>
        <ModelingResult v-else />
      </v-col>
    </v-row>
    <!-- dialog -->
    <v-dialog v-model="dialog" persistent max-width="400px">
      <v-card>
        <v-container fluid>
          <span class="headline">Name of Case</span>
          <!-- 최상단 메뉴 탭 -->

          <v-text-field v-model="caseName" placeholder="Case 1" required></v-text-field>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="dialog = !dialog" color="gray darken-1" text>
              Close
            </v-btn>
            <v-btn @click="saveModel" color="blue darken-1" @click.once="eventHandler" text>
              Confirm
            </v-btn>
          </v-card-actions>
        </v-container>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script>
import axios from "axios";

import { eventBus } from "@/main";
import ModelingSide from "@/components/modeling/ModelingSide.vue";
import Canvas from "@/components/modeling/Canvas.vue";
import FlowChart from "@/components/modeling/FlowChart.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import ModelingResult from "@/components/modeling/ModelingResult.vue";
import SaveMenu from "@/components/modeling/SaveMenu.vue";
import ModelingResultSide from "@/components/modeling/ModelingResultSide.vue";

export default {
  data() {
    return {
      caseName: "",
      showCanvas: true,
      dialog: false,

      left: null,
      top: null,
      modelingProcess: true,
      modelingOption: null
    };
  },
  components: {
    ModelingSide,
    Canvas,
    FlowChart,
    ModelingResult,
    ModelingResultSide,
    SaveMenu
  },
  methods: {
    runModel() {
      eventBus.$emit("runModel", true); // to Canvas.vue
      this.modelingProcess = !this.modelingProcess;
    },
    saveModel() {
      let path = "http://localhost:5000/saveModel";
      axios({
        method: "post",
        url: path,
        data: {
          caseName: this.caseName,
          modelingOption: this.modelingOption,
          // graphSources: JSON.stringify(this.graphSources),
          modelingSummary: JSON.stringify(this.modelingSummary)
        }
      });

      this.dialog = !this.dialog;
    },
    getPos(e) {
      let obj = e.target;
      this.left = obj.getBoundingClientRect().left;
      this.top = obj.getBoundingClientRect().top;
    }
  },
  computed: {
    ...mapState({
      inputs: state => state.modelingData.inputs,
      targets: state => state.modelingData.targets,
      graphSources: state => state.modelingResult.graphSources,
      modelingSummary: state => state.modelingResult.modelingSummary
    })
  },
  created() {
    eventBus.$on("inputFeatures", inputFeatures => {
      this.inputFeatures = inputFeatures;
    });
    eventBus.$on("targetFeatures", targetFeatures => {
      this.targetFeatures = targetFeatures;
    });
    eventBus.$on("showModelingResult", status => {
      this.showCanvas = !this.showCanvas;
    });
    eventBus.$on("modelingOption", modelingOption => {
      this.modelingOption = modelingOption;
    });
  },

  mounted() {}
};
</script>
