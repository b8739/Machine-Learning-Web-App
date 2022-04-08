<template>
  <div class="text-center">
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="" elevation="none" v-bind="attrs" v-on="on">
          <v-icon>mdi-content-save-outline</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in items"
          :key="index"
          link
          @click="clickSaveOptionEvent(index)"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <DefineDataset />
  </div>
</template>
<script>
import axios from "axios";
import { eventBus } from "@/main";
import DefineDataset from "@/components/modal/DefineDataset";
import { mapActions, mapState, mapGetters, mapMutations } from "vuex";

export default {
  data() {
    return {
      items: [{ title: "Overwrite" }, { title: "Save as New Dataset" }],
      dialog: false
    };
  },
  components: { DefineDataset },
  computed: {
    ...mapState({
      columns: state => state.initialData.columns,
      duplicatedColumns: state => state.summaryTableHandler.duplicatedColumns,
      tableName: state => state.initialData.tableName,
      summarizedInfo: state => state.initialData.summarizedInfo,
      tableChangeFlag: state => state.dataTableHandler.tableChangeFlag
    }),
    ...mapGetters("summaryTableHandler", ["summaryChangeNameFlag"])
  },
  methods: {
    ...mapActions("summaryTableHandler", ["calculateTransaction"]),
    ...mapActions("summaryTableHandler", ["summaryChangeTypeFlag"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapActions("initialData", ["loadColumns"]),
    ...mapActions("summaryTableHandler", ["cloneOriginalArray"]),

    clickSaveOptionEvent(index) {
      if (index == 0) {
        this.saveTableAxios("overwrite");
      } else {
        // this.saveTableAxios("newDataset");
        this.dialog = true;
        eventBus.$emit("saveNewFileMode", this.dialog);
      }
    }
  },
  created() {
    eventBus.$on("saveChanges", status => {
      this.saveTableAxios("overwrite");
    });
  }
};
</script>
