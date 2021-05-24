<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2">
        <ModelingSide />
      </v-col>
      <v-col cols="10">
        <v-toolbar elevation="1" dense>
          <v-spacer></v-spacer
          ><v-btn @click="runModel"
            ><v-icon left small>mdi-play-outline</v-icon> Run</v-btn
          ></v-toolbar
        >
        <Canvas v-if="showCanvas"></Canvas>
        <ModelingResult v-if="showModelingResult" />
      </v-col>
    </v-row>
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

export default {
  data() {
    return {
      left: null,
      top: null,
      showCanvas: true,
      showModelingResult: false
    };
  },
  components: {
    ModelingSide,
    Canvas,
    FlowChart,
    ModelingResult
  },
  methods: {
    ...mapMutations("modelingResult", ["saveGraphSources"]),
    ...mapMutations("modelingResult", ["saveModelingSummary"]),
    runModel() {
      this.showCanvas = !this.showCanvas;
      this.showModelingResult = !this.showModelingResult;
      const path = "http://localhost:5000/xgBoostModeling";
      axios
        .get(path)
        .then(res => {
          this.saveGraphSources(res.data[0]);
          this.saveModelingSummary(res.data[1]);
          // eventBus.$emit("graphSources", res.data[0]);
          // eventBus.$emit("modelingSummary", res.data[1]);
        })
        .catch(error => {
          console.error(error);
        });
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
      targets: state => state.modelingData.targets
    })
  },
  created() {
    eventBus.$on("inputFeatures", inputFeatures => {
      this.inputFeatures = inputFeatures;
    });
    eventBus.$on("targetFeatures", targetFeatures => {
      this.targetFeatures = targetFeatures;
    });
  },

  mounted() {}
};
</script>
