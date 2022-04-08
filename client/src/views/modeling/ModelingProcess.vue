<template>
  <div>
    <Header></Header>

    <v-container fluid>
      <v-row>
        <v-col>
          <Canvas></Canvas>
          <!-- <CanvasExample></CanvasExample> -->
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
import CanvasExample from "@/components/modeling/CanvasExample.vue";
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
    CanvasExample,
    Canvas
  },
  methods: {
    ...mapMutations("modelingData", ["saveGraphSources"]),
    ...mapMutations("modelingData", ["saveModelingSummary"]),
    ...mapMutations("modelingData", ["showProgressBar"]),
    saveModelingDraft() {
      eventBus.$emit("saveModelingDraft", true);
    },
    tellConnectAll() {
      eventBus.$emit("tellConnectAll", true);
    },
    runModel() {
      eventBus.$emit("saveRequest_canvas", true); // to Canvas.vue
      this.showProgressBar(true);
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
      splitRatio: state => state.modelingData.splitRatio,
      progressBar: state => state.modelingData.progressBar
    })
  },

  created() {}
};
</script>
