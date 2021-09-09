<template>
  <v-dialog v-model="dialog" width="100%" persistent class="ma-0">
    <v-container fill-height fluid class="pa-0">
      <v-navigation-drawer v-model="drawer" width="15%" height="100vh" :mini-variant.sync="mini">
        <v-list dense>
          <v-list-group v-model="depthStatus">
            <template v-slot:activator>
              <v-list-item-title active>Structure</v-list-item-title>
            </template>
            <v-list-item link>
              <v-list-item-icon>
                <v-icon></v-icon>
              </v-list-item-icon>
              <v-list-item-title draggable label>Traces</v-list-item-title>
            </v-list-item>
            <v-list-item link>
              <v-list-item-icon>
                <v-icon></v-icon>
              </v-list-item-icon>
              <v-list-item-title label>Subplots</v-list-item-title>
            </v-list-item>
          </v-list-group>
        </v-list>
      </v-navigation-drawer>
      <v-main>
        <v-container fluid fill-height class="pa-0">
          <v-row>
            <!-- 2nd -->
            <v-col cols="3" class="pa-0 ma-0">
              <v-card class="pa-0 ma-0" height="100vh">
                <v-container fluid>
                  <v-row justify="end">
                    <v-col class="pa-0 ma-0" cols="5"
                      ><v-btn @click="numTracePanel++">+ Trace</v-btn></v-col
                    ></v-row
                  >
                  <v-row>
                    <v-expansion-panels multiple>
                      <v-col>
                        <v-expansion-panel
                          v-for="(tracePanel, tpIndex) in numTracePanel"
                          :key="tpIndex"
                        >
                          <v-expansion-panel-header> Trace {{ tpIndex }} </v-expansion-panel-header>
                          <v-expansion-panel-content>
                            <v-container fluid>
                              <v-row>
                                <v-col class="pa-0 ma-0" cols="3">
                                  <v-subheader>Type</v-subheader></v-col
                                >
                                <v-col class="pa-0 ma-0" cols="9">
                                  <v-select dense></v-select></v-col
                              ></v-row>
                              <v-row v-for="(axisType, atIndex) in axisTypes" :key="atIndex">
                                <!-- x -->
                                <v-col class="pa-0 ma-0" cols="3">
                                  <v-subheader>{{ axisType }}</v-subheader></v-col
                                >
                                <v-col class="pa-0 ma-0" cols="9">
                                  <v-select
                                    @change="
                                      featureName => loadAxis(featureName, axisType, tpIndex)
                                    "
                                    :items="columns"
                                    dense
                                  ></v-select
                                ></v-col>
                              </v-row>
                            </v-container>
                          </v-expansion-panel-content>
                        </v-expansion-panel>
                      </v-col>
                    </v-expansion-panels>
                  </v-row>
                </v-container>
              </v-card>
            </v-col>

            <v-col class="pa-0 ma-0">
              <v-card>
                <PlotlyEdaGraph :graphWidth="600" :graphHeight="400" :isEdit="false" /> </v-card
            ></v-col>
          </v-row>
        </v-container>
      </v-main>
      <!-- <v-navigation-drawer height="100vh" v-model="drawer" absolute>
      je
    </v-navigation-drawer> -->
    </v-container>
  </v-dialog>
</template>
<script>
import { eventBus } from "@/main";
import PlotlyEdaGraph from "@/components/graph/PlotlyEdaGraph.vue";

import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      axisTypes: ["x", "y"],
      numTracePanel: 1,
      dialog: true,
      drawer: true,
      depthStatus: true,
      mini: false
    };
  },
  methods: {
    loadAxis(featureName, axisType, tpIndex) {
      let payload = { featureName: featureName, axisType: axisType, tpIndex: tpIndex };
      eventBus.$emit("load_xAxis", payload);
      // let path = "http://localhost:5000/loadEditGraphData";
      // // axios
      // this.$axios({
      //   method: "post",
      //   url: path,
      //   data: {
      //     featureName: featureName,
      //     tableName: this.tableName
      //   }
      // })
      //   .then(res => {
      //     this.updatePlot(res.data[featureName], axisType);
      //   })
      //   .catch(error => {
      //     console.error(error);
      //   });
    }
  },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns
    })
  },
  components: {
    PlotlyEdaGraph
  },
  created() {
    eventBus.$on("openDialog", dialogStatus => {
      this.dialog = dialogStatus;
    });
  }
};
</script>
