<template>
  <div data-app>
    <v-row justify="center">
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
          <v-card outlined>
            <v-layout>
              <!-- 좌측 -->
              <v-flex xs2>
                <ColumnList :columns="columns" :styleObject="style_columnList">
                  <v-subheader>{{ columns.length }} 개 열</v-subheader>
                </ColumnList>
              </v-flex>
              <v-divider vertical></v-divider>
              <!-- 우측 -->
              <v-flex xs8>
                <!-- 우측 - 상단 -->

                <v-flex><GraphTypeToolbar /></v-flex>
                <!-- 우측 - 하단 -->
                <!-- 우측 - 하단 - 좌측-->
                <v-container>
                  <v-row>
                    <v-col cols="2" class="axisTitle"
                      ><DragBoxYaxis :styleObject="style_Dragbox_yaxis" axisPosition="top" />
                      <DragBoxYaxis :styleObject="style_Dragbox_yaxis" axisPosition="middle">
                        Y
                      </DragBoxYaxis>
                      <DragBoxYaxis :styleObject="style_Dragbox_yaxis" axisPosition="bottom" />
                    </v-col>
                    <v-col cols="10"> <ApexChart :graphHeight="500"/></v-col>
                    <v-col cols="2"></v-col>
                    <v-col cols="2">
                      <DragBoxXaxis :styleObject="style_DragBox_xaxis" axisPosition="left" />
                    </v-col>
                    <v-col cols="3" class="axisTitle">
                      <DragBoxXaxis :styleObject="style_DragBox_xaxis" axisPosition="middle"
                        ><span> X</span>
                      </DragBoxXaxis>
                    </v-col>
                    <v-col cols="3">
                      <DragBoxXaxis :styleObject="style_DragBox_xaxis" axisPosition="right" />
                    </v-col>
                  </v-row>
                </v-container>
                <!-- layout 변경 -->
                <!-- 우측 - 하단 - 우측-->
                <v-flex>
                  <v-layout column> <v-flex></v-flex></v-layout
                ></v-flex>
              </v-flex>

              <div style="height:300px;background-color:red"></div>
            </v-layout>
          </v-card>
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
import GraphTypeToolbar from "@/components/eda/GraphTypeToolbar.vue";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      dialog: false,
      style_columnList: {
        height: "300px",
        "overflow-y": "scroll"
      },
      style_DragBox_xaxis: {
        // border: "1px solid lightgray",
        // width: "100px",
        height: "50px"
      },
      style_Dragbox_yaxis: {
        // border: "1px solid lightgray",
        height: "100px"
        // width: "100px"
      },
      xColumns: ["Drag X axis Here"],
      yColumns: ["Drag Y axis Here"]
    };
  },
  props: ["columns"],
  components: {
    ColumnList,
    DragBoxXaxis,
    DragBoxYaxis,
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
  text-align: center;
}
</style>
