<template>
  <v-list dense>
    <v-list-group v-model="activeState">
      <template v-slot:activator>
        <v-list-item-title active>Edit Feature</v-list-item-title>
      </template>
      <v-list-item
        :disabled="item.title == 'Moving Average' || item.title == 'Change Type'"
        v-for="item in items"
        :key="item.title"
        link
        @click="callOption(item.title)"
      >
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
      columns: state => state.initialData.columns,
      duplicatedColumns: state => state.summaryTableHandler.duplicatedColumns
    })
  },
  methods: {
    ...mapMutations("preprocessHandler", ["setPreprocessStatus"]),
    ...mapMutations("preprocessHandler", ["setEditStatus"]),
    ...mapMutations("summaryTableHandler", ["setDialog"]),

    ...mapMutations("preprocessHandler", ["setEvent"]),
    ...mapMutations("preprocessHandler", ["setAdditionalCancelEvent"]),
    ...mapMutations("preprocessHandler", ["resetPreprocessVuex"]),
    ...mapActions("preprocessHandler", ["cancelEvent"]),
    ...mapActions("preprocessHandler", ["activateEvent"]),
    ...mapActions("summaryTableHandler", ["cloneOriginalArray"]),
    ...mapActions("summaryTableHandler", ["revertToBackupArray"]),
    ...mapActions("summaryTableHandler", ["backupColumns"]),

    confirmNameChange() {
      this.setEditStatus(false);
      this.setPreprocessStatus(null);
      this.setAdditionalCancelEvent(null);
      this.backupColumns();
    },
    callOption(title) {
      this.cancelEvent();
      // this.resetPreprocessVuex();
      if (title == "Change Name") {
        this.activateEvent("summaryChangeName");
        this.setEvent(this.confirmNameChange);
        this.setAdditionalCancelEvent(this.revertToBackupArray);
      } else if (title == "Change Type") {
        this.activateEvent("summaryChangeType");
      } else if (title == "Change Order") {
        this.activateEvent("summaryChangeOrderModal");
        this.backupColumns();
        this.setAdditionalCancelEvent(this.revertToBackupArray);
        this.setDialog(true);
        // confirm시
        this.setEvent(() => {
          this.setDialog(false);
          this.setAdditionalCancelEvent(null);
        });
      }
    }
  }
};
</script>
