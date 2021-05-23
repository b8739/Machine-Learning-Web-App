<template>
  <v-data-table
    v-if="modelingSummary"
    :headers="headers"
    :items="dataTableItems"
    class="elevation-1"
  ></v-data-table>
</template>
<script>
import { eventBus } from "@/main";
export default {
  data() {
    return {
      modelingSummary: false,
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
    eventBus.$on("modelingSummary", modelingSummary => {
      this.modelingSummary = modelingSummary;
    });
  }
};
</script>
