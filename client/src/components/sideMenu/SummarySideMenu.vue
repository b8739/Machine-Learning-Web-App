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
    dataFeatures() {
      return this.$root.$refs.dataFeatures;
    },

    ...mapState({
      tableName: state => state.initialData.tableName,
      datasetSize: state => state.initialData.datasetSize,
      editStatus: state => state.preprocessHandler.editStatus,
      preprocessStatus: state => state.preprocessHandler.preprocessStatus
    })
  },
  methods: {
    ...mapMutations("preprocessHandler", ["setPreprocessStatus"]),
    ...mapMutations("preprocessHandler", ["setEditStatus"]),
    ...mapMutations("preprocessHandler", ["setEvent"]),
    ...mapActions("preprocessHandler", ["cancelEvent"]),
    ...mapMutations("preprocessHandler", ["setAdditionalCancelEvent"]),
    revertNameChange() {
      if (!(JSON.stringify(this.columns) === JSON.stringify(this.dataFeatures.duplicatedColumns)))
        //false, 동일하지 않을 때
        this.dataFeatures.duplicateColumns();
    },
    callOption(title) {
      if (title == "Change Name") {
        this.cancelEvent();
        this.setPreprocessStatus("summaryChangeName");
        this.setEditStatus(true);
        this.setAdditionalCancelEvent(this.revertNameChange);
      } else if (title == "Change Type") {
        this.cancelEvent();
        this.setPreprocessStatus("summaryChangeType");
        this.setEditStatus(true);
      } else if (title == "Change Order") {
        eventBus.$emit("openChangeOrderModal", true);
        // this.setPreprocessStatus("summary-change-order");
      }
      // if (title == "Moving Average") {
      //   eventBus.$emit("openMovingAverageModal", true);
      // }
    }
  }
};
</script>
