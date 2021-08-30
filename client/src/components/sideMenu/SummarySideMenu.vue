<template>
  <v-list dense>
    <v-list-group v-model="activeState">
      <template v-slot:activator>
        <v-list-item-title active>Edit Feature</v-list-item-title>
      </template>
      <v-list-item v-for="item in items" :key="item.title" link @click="callOption(item.title)">
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-title draggable label>{{ item.title }}</v-list-item-title>
      </v-list-item>
    </v-list-group>
  </v-list>
</template>
<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import { eventBus } from "@/main";

export default {
  data() {
    return {
      activeState: true,
      items: [
        { title: "Change Name", icon: "mdi-pencil" },
        { title: "Change Order", icon: "mdi-swap-vertical" },
        { title: "Change Type", icon: "mdi-beaker-question-outline" },
        { title: "Moving Average", icon: "mdi-chart-timeline-variant" }
      ]
    };
  },
  computed: {
    SummaryTable() {
      return this.$root.$refs.SummaryTable;
    },

    ...mapState({
      tableName: state => state.initialData.tableName,
      datasetSize: state => state.initialData.datasetSize,
      editStatus: state => state.preprocessHandler.editStatus,
      preprocessStatus: state => state.preprocessHandler.preprocessStatus,
      columns: state => state.initialData.columns
    })
  },
  methods: {
    ...mapMutations("preprocessHandler", ["setPreprocessStatus"]),
    ...mapMutations("preprocessHandler", ["setEditStatus"]),
    ...mapMutations("preprocessHandler", ["setEvent"]),
    ...mapMutations("preprocessHandler", ["setAdditionalCancelEvent"]),
    ...mapActions("preprocessHandler", ["cancelEvent"]),
    ...mapActions("preprocessHandler", ["activateEvent"]),

    revertNameChange() {
      console.log("revert");
      if (!(JSON.stringify(this.columns) === JSON.stringify(this.SummaryTable.duplicatedColumns)))
        //false, 동일하지 않을 때
        this.SummaryTable.duplicateColumns(this.SummaryTable.duplicatedColumns, this.columns);
    },
    confirmNameChange() {
      this.setEditStatus(false);
      this.setPreprocessStatus(null);
      this.setAdditionalCancelEvent(null);
    },
    callOption(title) {
      this.cancelEvent();
      if (title == "Change Name") {
        this.activateEvent("summaryChangeName");
        this.setAdditionalCancelEvent(this.revertNameChange);
        this.setEvent(this.confirmNameChange);
      } else if (title == "Change Type") {
        this.activateEvent("summaryChangeType");
      } else if (title == "Change Order") {
        this.activateEvent("summaryChangeOrderModal");
        this.setEvent(function() {});
        eventBus.$emit("openChangeOrderModal", true);
      }
    }
  }
};
</script>
