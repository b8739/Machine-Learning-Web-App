<template>
  <div>
    <Header></Header>

    <v-app>
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

              <v-btn @click="dialog = true">Save Model</v-btn>
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

              <v-text-field v-model="case_name" placeholder="Case 1" required></v-text-field>
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
        <SaveChange />
      </v-container>
    </v-app>
  </div>
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
import SaveChange from "@/components/save/SaveChange.vue";
import ModelingResultSide from "@/components/modeling/ModelingResultSide.vue";

export default {
  data() {
    return {
      case_name: "",
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
    SaveMenu,
    SaveChange
  },
  methods: {
    ...mapMutations("modelingResult", ["saveCaseList"]),

    loadCases() {
      console.log("loadCases");
      let path = "http://localhost:5000/loadCases";
      axios
        .get(path)
        .then(res => {
          this.saveCaseList(res.data);
        })
        .catch(error => {});
    },
    runModel() {
      eventBus.$emit("runModel", true); // to Canvas.vue
      this.modelingProcess = !this.modelingProcess;
    },
    saveModel() {
      let vm = this;
      let path = "http://localhost:5000/saveModel";
      axios({
        method: "post",
        url: path,
        data: {
          case_name: this.case_name,
          modelingOption: this.modelingOption,
          snippet: this.snippet,
          graphSources: JSON.stringify(this.graphSources),
          modelingSummary: JSON.stringify(this.modelingSummary)
        }
      }).then(function(res) {
        vm.loadCases();
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
      snippet: state => state.modelingData.snippet,
      graphSources: state => state.modelingResult.graphSources,
      modelingSummary: state => state.modelingResult.modelingSummary
    })
  },

  created() {
    let caseNameFromUrl = this.$route.params.case;
    // console.log(caseNameFromUrl);
    if (caseNameFromUrl != null) {
      this.showCanvas = false;
      this.modelingProcess = false;

      eventBus.$emit("changeCase", caseNameFromUrl);
    }
    // eventbus
    eventBus.$on("inputFeatures", inputFeatures => {
      this.inputFeatures = inputFeatures;
    });
    eventBus.$on("targetFeatures", targetFeatures => {
      this.targetFeatures = targetFeatures;
    });
    eventBus.$on("showModelingResult", status => {
      this.showCanvas = false;
    });
    eventBus.$on("modelingOption", modelingOption => {
      this.modelingOption = modelingOption;
    });
  }
  // beforeRouteLeave(to, from, next) {
  //   eventBus.$emit("openSaveChange", true);

  //   next(false);
  // }
};
</script>
