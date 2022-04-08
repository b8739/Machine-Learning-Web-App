<template>
  <v-dialog v-model="dialog">
    <div data-app>
      <v-card>
        <v-toolbar color="light">
          <v-btn icon dark @click="dialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-spacer></v-spacer>
          <v-toolbar-title>EDA Graph Builder (기능 미완성)</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn text @click="dialog = false">
              Save
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <v-container fluid>
          <!-- 좌측 -->
          <v-row>
            <v-col cols="2">
              <ColumnList :style="style_columnList">
                <v-subheader>{{ columns.length }} 개 열</v-subheader>
              </ColumnList>
            </v-col>
            <v-divider vertical></v-divider>
            <!-- 우측 -->
            <v-col cols="10">
              <!-- 우측 상단 -->
              <v-row>
                <v-col cols="12"><GraphTypeToolbar /></v-col>
                <v-col cols="7" offset="1" class="axisTitle">
                  <v-card class="ml-5" height="50px">
                    <Xgroup :styleObject="style_DragBox_xaxis" />
                  </v-card>
                </v-col>
              </v-row>
              <!-- 우측 중앙 -->
              <v-row dense>
                <v-col cols="1" class=" ml-4 axisTitle" align-self="center">
                  <v-card height="400px">
                    <DragBoxYaxis :styleObject="style_Dragbox_yaxis" />
                  </v-card>
                </v-col>

                <v-col cols="7" class="apexChartWrapper">
                  <!-- <span class="yLabel">Y</span> -->

                  <!-- <ApexChart v-show="apexChartRender" /> -->
                  <PlotlyEdaGraph :graphWidth="800" :graphHeight="400" :isEdit="false" />
                </v-col>

                <!-- 원래 500, grouping 개발하느라 임시로 작게 변경 -->
              </v-row>
              <!-- 우측 하단 -->
              <v-row dense>
                <v-col cols="7" offset="1" class="axisTitle" :style="{ width: '500px' }">
                  <v-card class="ml-5" height="50px">
                    <!-- <span class="xLabel"> X</span> -->
                    <DragBoxXaxis :styleObject="style_DragBox_xaxis"> </DragBoxXaxis>
                  </v-card>
                </v-col>
              </v-row>
            </v-col>
          </v-row>

          <!-- 우측 -->
        </v-container>
      </v-card>
    </div>
  </v-dialog>
</template>
<script>
import ColumnList from "@/components/eda/ColumnList.vue";
// import ApexChart from "@/components/eda/ApexChart.vue";
import PlotlyEdaGraph from "@/components/graph/PlotlyEdaGraph.vue";
import DragBoxXaxis from "@/components/eda/DragBoxXaxis.vue";
import DragBoxYaxis from "@/components/eda/DragBoxYaxis.vue";
import Xgroup from "@/components/eda/Xgroup.vue";
import GraphTypeToolbar from "@/components/eda/GraphTypeToolbar.vue";

import { eventBus } from "@/main";
// vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      dialog: false,
      style_columnList: {
        height: "300px",
        "overflow-y": "scroll"
      },
      style_DragBox_xaxis: {
        border: "1px solid lightgray",
        // width: "100px",
        height: "50px"
      },
      style_Dragbox_yaxis: {
        border: "1px solid lightgray",
        height: "200px"
        // width: "100px"
      },
      xColumns: ["Drag X axis Here"],
      yColumns: ["Drag Y axis Here"],
      apexChartRender: true,
      syncChartRender: false
    };
  },
  // props: ["columns"],
  computed: {
    ...mapState("initialData", ["columns"])
  },
  methods: {
    ...mapMutations("initialData", ["setNavStatus"])
  },
  components: {
    ColumnList,
    DragBoxXaxis,
    DragBoxYaxis,
    Xgroup,
    ApexChart,
    GraphTypeToolbar,
    PlotlyEdaGraph
  },
  created() {
    // eventBus.$on("openDialog", dialogStatus => {
    //   this.dialog = dialogStatus;
    // });
  }
};
</script>
<style scoped>
.axisTitle {
  /* border: 1px solid red; */
  text-align: center;
}
.apexChartWrapper {
  /* position: relative; */
}
.yLabel {
  position: absolute;
  top: 45%;
  left: 0;
}
.xLabel {
  position: absolute;
  top: -40%;
  left: 45%;
}
.groupXlabel {
  position: absolute;
  top: 40%;
  left: 45%;
}
</style>
