<template>
  <v-data-table :headers="headers" :items="dataTableItems" class="elevation-1"></v-data-table>
</template>
<script>
import { eventBus } from "@/main";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      // showModelingSummary: false,
      headers: [
        {
          text: "Modeling Summary",
          align: "start",
          sortable: false,
          value: "name"
        },
        { text: "Value", value: "value" }
      ]
    };
  },
  computed: {
    ...mapState({
      modelingSummary: state => state.modelingResult.modelingSummary
    }),
    dataTableItems() {
      let dataTableItems = [];
      let dataTableFormat = {};
      for (const [key, value] of Object.entries(this.modelingSummary)) {
        dataTableFormat = { name: key, value: value };
        dataTableItems.push(dataTableFormat);
      }

      return dataTableItems;
    }
  },
  created() {
    // eventBus.$on("showModelingSummary", status => {
    //   this.showModelingSummary = status;
    // });
  }
};
</script>
