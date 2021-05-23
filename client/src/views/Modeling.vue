<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2">
        <ModelingSide />
      </v-col>
      <v-col cols="10">
        <!-- <v-card min-height="800px" elevation="1">
          <v-toolbar elevation="1" dense>
            <v-spacer></v-spacer
            ><v-btn><v-icon left small>mdi-play-outline</v-icon> Run</v-btn></v-toolbar
          >
          <v-container>
            <v-row justify="center">
              <v-col cols="2" v-for="(input, index) in inputs" :key="index">
                <v-card-text class="pa-0">{{ input }}</v-card-text>
                <v-chip draggable label>
                  Input
                </v-chip>
              </v-col>
              <v-col cols="2" v-for="(target, index) in targets" :key="index">
                <v-card-text class="pa-0">{{ target }}</v-card-text>
                <v-chip draggable label>
                  Target
                </v-chip>
              </v-col>
            </v-row>
          </v-container>
        </v-card> -->
        <v-toolbar elevation="1" dense>
          <v-spacer></v-spacer
          ><v-btn @click="runModel"
            ><v-icon left small>mdi-play-outline</v-icon> Run</v-btn
          ></v-toolbar
        >
        <!-- <Canvas></Canvas> -->
        <ModelingResult />
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
      top: null
    };
  },
  components: {
    ModelingSide,
    Canvas,
    FlowChart,
    ModelingResult
  },
  methods: {
    runModel() {
      const path = "http://localhost:5000/xgBoostModeling";
      axios
        .get(path)
        .then(res => {
          // console.log(res.data);
          eventBus.$emit("modelResult", res.data);
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
