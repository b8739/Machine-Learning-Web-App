<template>
  <div>
    <Header></Header>

    <v-container fluid>
      <v-row>
        <!-- <v-col cols="2">
          <ModelingSide />
        </v-col> -->
        <v-col>
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
    ...mapMutations("modelingData", ["saveGraphSources"]),
    ...mapMutations("modelingData", ["saveModelingSummary"]),

    runModel() {
      eventBus.$emit("saveRequest_canvas", true); // to Canvas.vue
      eventBus.$emit("saveRequest_canvasSide", true); // to Canvas.vue
    },

    getPos(e) {
      let obj = e.target;
      this.left = obj.getBoundingClientRect().left;
      this.top = obj.getBoundingClientRect().top;
    }
  },
  computed: {
    ...mapState({
      modelingRequest: state => state.modelingData.modelingRequest,
      splitRatio: state => state.modelingData.splitRatio
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
