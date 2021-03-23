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
            <v-row>
              <v-col cols="2"><ColumnList /></v-col>
              <v-col cols="6"> <ApexChart :graphHeight="500"/></v-col>
            </v-row>
          </v-card>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>
<script>
import ColumnList from "@/components/eda/ColumnList.vue";
import ApexChart from "@/components/eda/ApexChart.vue";
export default {
  data() {
    return {
      dialog: false
    };
  },
  components: {
    ColumnList,
    ApexChart
  }
};
</script>
