<template>
  <v-container>
    <v-row dense>
      <v-col cols="12"> <v-checkbox label="Target" @change="selectAll"></v-checkbox></v-col>
    </v-row>
    <v-row dense>
      <v-col>
        <div class="columnList">
          <v-checkbox
            v-for="(column, columnIndex) in columns"
            :key="columnIndex"
            v-model="targets"
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
      selected: [],
      disabledProps: {
        disabled: true
      },
      targets: []
    };
  },
  props: [],

  methods: {
    ...mapMutations("modelingData", ["saveTargets"]),
    selectAll() {
      for (let i = 0; i < this.columns.length; i++) {
        this.targets.push(this.columns[i]);
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
      console.log(columnIndex);
      eventBus.$emit("targetColumnChecked", columnIndex);
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
    ...mapGetters("initialData", ["columns"]),
    withoutUndefined() {
      let cleansed = [];
      this.targets.forEach(element => {
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
    },
    ...mapState({})
  },
  created() {
    eventBus.$on("inputColumnChecked", index => {
      this.selected.push(index);
    });
    eventBus.$on("stepTwoFinished", status => {
      this.saveTargets(this.withoutUndefined);
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
