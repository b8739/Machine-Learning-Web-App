<template>
  <div data-app>
    <v-row justify="center">
      <v-dialog v-model="dialog" fullscreen hide-overlay transition="dialog-bottom-transition">
        <!-- Trigger 버튼 -->
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="primary" dark v-bind="attrs" v-on="on">
            Open Dialog
          </v-btn>
        </template>
        <v-card>
          <v-toolbar color="primary">
            <v-btn icon dark @click="dialog = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
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
              <v-flex xs2>
                <ColumnList :columns="columns" :styleObject="style_columnList">
                  <v-subheader>{{ columns.length }} 개 열</v-subheader>
                </ColumnList></v-flex
              >
              <v-divider vertical></v-divider>
              <v-flex xs6>
                <v-layout row>
                  <v-flex
                    ><DragBoxYaxis :columns="xColumns" :styleObject="style_Dragbox_yaxis"
                  /></v-flex>
                  <v-flex>
                    <v-layout column
                      ><v-flex><ApexChart :graphHeight="500"/></v-flex>
                      <v-flex
                        ><DragBoxXaxis
                          :columns="xColumns"
                          :styleObject="style_DragBox_xaxis"/></v-flex></v-layout
                  ></v-flex>
                </v-layout>
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
export default {
  data() {
    return {
      dialog: false,
      emptyColumns: ["."],
      xColumns: [1, 2, 3],
      style_columnList: {
        height: "300px",
        "overflow-y": "scroll"
      },
      style_DragBox_xaxis: {
        height: "300px"
      },
      style_Dragbox_yaxis: {
        height: "300px",
        width: "40px"
      }
    };
  },
  props: ["columns"],
  components: {
    ColumnList,
    DragBoxXaxis,
    DragBoxYaxis,
    ApexChart
  }
};
</script>
