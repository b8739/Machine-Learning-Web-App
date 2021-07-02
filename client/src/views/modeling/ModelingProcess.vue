<template>
  <div>
    <Header></Header>

    <v-container fluid>
      <v-row>
        <v-col cols="2">
          <ModelingSide />
        </v-col>
        <v-col cols="10">
          <v-toolbar elevation="1" dense>
            <v-spacer></v-spacer
            ><v-btn @click="runModel"><v-icon left small>mdi-play-outline</v-icon> Run</v-btn>
          </v-toolbar>
          <Canvas></Canvas>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import axios from "axios";

import { eventBus } from "@/main";
import ModelingSide from "@/components/modeling/ModelingSide.vue";
import Canvas from "@/components/modeling/Canvas.vue";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      modelingProcess: true,
      modelingParameter: null
    };
  },
  components: {
    ModelingSide,
    Canvas
  },
  methods: {
    runModel() {
      eventBus.$emit("runModel", true); // to Canvas.vue
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
      algorithm: state => state.modelingData.algorithm
    })
  },

  created() {
    // eventbus
    eventBus.$on("inputFeatures", inputFeatures => {
      this.inputFeatures = inputFeatures;
    });
    eventBus.$on("targetFeatures", targetFeatures => {
      this.targetFeatures = targetFeatures;
    });
    eventBus.$on("modelingParameter", modelingParameter => {
      this.modelingParameter = modelingParameter;
    });
  }
  // beforeRouteLeave(to, from, next) {
  //   eventBus.$emit("openSaveChange", true);

  //   next(false);
  // }
};
</script>
