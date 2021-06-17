<template>
  <v-row>
    <v-col>
      <div class="columnList">
        <v-checkbox
          v-for="(column, columnIndex) in columns"
          :key="columnIndex"
          :label="column"
          v-model="selected[columnIndex]"
          :value="column"
          dense
        >
        </v-checkbox>
      </div>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="stepOneComplete">
          Continue
        </v-btn>

        <v-btn text @click="closeDialog">
          Cancel
        </v-btn>
      </v-card-actions>
    </v-col>
  </v-row>
</template>
<script>
import { mapState, mapGetters } from "vuex";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      clickedColumnIndex: null,
      unClickedColumnItemStyle: {
        // "background-color": "none"
      },
      clickedColumnItemStyle: {
        "background-color": "lightgrey"
      },
      selected: []
    };
  },
  props: [],

  methods: {
    closeDialog() {
      eventBus.$emit("closeDialog", false);
    },
    stepOneComplete() {
      eventBus.$emit("toStepTwo", 2);
      eventBus.$emit("selectedColumns", this.selectedWithoutNull);
    },
    changeColor(columnIndex) {
      this.clickedColumnIndex = columnIndex;
    },
    dynamicColumnStyle(columnIndex) {
      if (this.clickedColumnIndex == columnIndex) {
        return this.clickedColumnItemStyle;
      } else return this.unClickedColumnItemStyle;
    }
  },
  components: {},
  computed: {
    selectedWithoutNull() {
      let selected = [];
      this.selected.forEach(element => {
        if (element != undefined || element != null) {
          selected.push(element);
        }
      });
      return selected;
    },
    ...mapState({
      dataset: state => state.initialDatadataset

      // columns: state => state.columns
    }),
    ...mapGetters("initialData", ["columns", "indexNum"])
  }
};
</script>
<style scoped>
.columnList {
  height: 230px;
  overflow-y: scroll;
}
</style>
