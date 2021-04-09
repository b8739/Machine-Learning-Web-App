<template>
  <div data-app>
    <v-row class="vrowContainer">
      <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <!-- Trigger 버튼 -->
        <!-- <template v-slot:activator="{ on, attrs }">
          <button v-on="on">hi</button>
          <v-btn color="primary" dark v-bind="attrs" v-on="on">
            EDA
          </v-btn>
        </template> -->
        <v-card>
          <v-toolbar color="primary">
            <v-btn icon dark @click="dialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-spacer></v-spacer>
            <v-toolbar-title>EDA Graph Builder</v-toolbar-title>
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
                <ColumnList :columns="columns" :styleObject="style_columnList">
                  <v-subheader>{{ columns.length }} 개 열</v-subheader>
                </ColumnList>
              </v-col>
              <v-divider vertical></v-divider>

              <v-col cols="10">
                <v-col><GraphTypeToolbar /></v-col>
                <v-col cols="3" offset="3" class="axisTitle">
                  <span class="xLabel"> Group X</span>
                  <Xgroup :styleObject="style_DragBox_xaxis" />
                </v-col>
                <v-row justify="center">
                  <v-col cols="1" class="axisTitle" align-self="center">
                    <DragBoxYaxis :styleObject="style_Dragbox_yaxis" />
                  </v-col>

                  <v-col cols="8" class="apexChartWrapper">
                    <span class="yLabel">Y</span>
                    <ApexChart
                  /></v-col>
                  <!-- 원래 500, grouping 개발하느라 임시로 작게 변경 -->
                </v-row>
                <v-row justify="center">
                  <v-col cols="3" offset="3" class="axisTitle" :style="{ width: '500px' }">
                    <span class="xLabel"> X</span>
                    <DragBoxXaxis :styleObject="style_DragBox_xaxis"> </DragBoxXaxis>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>

            <!-- 우측 -->
          </v-container>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>
<script>
import ColumnList from "@/components/eda/ColumnList.vue";
import ApexChart from "@/components/eda/ApexChart.vue";
import DragBoxXaxis from "@/components/eda/DragBoxXaxis.vue";
import DragBoxYaxis from "@/components/eda/DragBoxYaxis.vue";
import Xgroup from "@/components/eda/Xgroup.vue";
import GraphTypeToolbar from "@/components/eda/GraphTypeToolbar.vue";
import { eventBus } from "@/main";
// vuex
import { mapActions } from "vuex";
import { mapGetters } from "vuex";
import { mapState } from "vuex";
import { mapMutations } from "vuex";
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
      yColumns: ["Drag Y axis Here"]
    };
  },
  props: ["columns"],
  computed: {
    ...mapState({})
  },
  components: {
    ColumnList,
    DragBoxXaxis,
    DragBoxYaxis,
    Xgroup,
    ApexChart,
    GraphTypeToolbar
  },
  created() {
    eventBus.$on("openDialogue", dialogStatus => {
      this.dialog = dialogStatus;
    });
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
</style>
