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
            <v-spacer></v-spacer>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn @click="tellConnectAll" v-bind="attrs" v-on="on" class="mr-2">
                  Connect All</v-btn
                >
              </template>
              <span>Connect Order (Input -> Algorithm -> Target)</span>
            </v-tooltip>

            <v-btn @click="runModel" color="primary"
              ><v-icon left small>mdi-play-outline</v-icon> Run</v-btn
            >
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
    tellConnectAll() {
      eventBus.$emit("tellConnectAll", true);
    },
    runModel() {
      eventBus.$emit("saveRequest_canvas", true); // to Canvas.vue
      eventBus.$emit("saveRequest_canvasSide", true); // to CanvasSide.vue
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
