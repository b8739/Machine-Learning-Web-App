<template>
  <v-container>
    <v-row dense>
      <v-col cols="12"> <v-checkbox label="Input" @change="selectAll"></v-checkbox></v-col>
    </v-row>
    <v-row dense>
      <v-col>
        <div class="columnList">
          <v-checkbox
            v-for="(column, columnIndex) in columns"
            v-model="inputs[columnIndex]"
            :key="columnIndex"
            :label="column"
            :value="column"
            @change="checkedEvent(columnIndex)"
            dense
            v-bind="dynamicProps(columnIndex)"
          >
          </v-checkbox>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
//vuex
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

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
      selected: [], //이미 Target에서 선택되어서, input에서는 선택할 수 없는 것들
      disabledProps: {
        disabled: true
      },
      //v-model
      inputs: []
    };
  },
  props: [],

  methods: {
    ...mapMutations("modelingData", ["saveInputs"]),
    selectAll() {
      for (let i = 0; i < this.columns.length; i++) {
        this.inputs.push(this.columns[i]);
      }
    },
    dynamicProps(columnIndex) {
      for (let i = 0; i < this.selected.length; i++) {
        if (this.selected[i] == columnIndex) {
          return this.disabledProps;
        }
      }
    },
    checkedEvent(columnIndex) {
      eventBus.$emit("inputColumnChecked", columnIndex);
    },
    closeDialog() {
      eventBus.$emit("closeDialog", false);
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
    ...mapGetters({
      columns: state => state.initialData.columns
    }),
    withoutUndefined() {
      let cleansed = [];
      this.inputs.forEach(element => {
        if (element != undefined) {
          cleansed.push(element);
        }
      });
      return cleansed;
    },
    selectedWithoutNull() {
      let selected = [];
      this.selected.forEach(element => {
        if (element != undefined || element != null) {
          selected.push(element);
        }
      });
      return selected;
    }
  },
  created() {
    //중복 체크 방지
    eventBus.$on("targetColumnChecked", index => {
      this.selected.push(index);
    });
    //vuex에 저장
    eventBus.$on("stepTwoFinished", status => {
      this.saveInputs(this.withoutUndefined);
    });
  }
};
</script>
<style scoped>
.columnList {
  height: 230px;
  overflow-y: scroll;
}
</style>
