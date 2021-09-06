<template
  ><div>
    <v-dialog v-model="dialog">
      <v-card v>
        <v-btn x-small right absolute min-width="20" min-height="30" @click="hideEditModal()"
          ><v-icon small>mdi-close</v-icon>
        </v-btn>
        <v-container>
          <v-card-text style="text-align:center" class="title">Graph Studio</v-card-text>
          <v-row justify="center" align="center">
            <PlotlyLine
              :seriesName="column"
              :editMode="true"
              :graphWidth="800"
              :graphHeight="500"
            />
          </v-row>
          <v-row> <DataTable /></v-row>
        </v-container>
      </v-card>
    </v-dialog>
    <!-- <portal to="destination">
      <TimeSeries
        v-if="dialog"
        :graphWidth="500"
        :graphHeight="500"
        :seriesName="column"
        :dialog="dialog"
      />
    </portal> -->
  </div>
</template>
<script>
import PlotlyLine from "@/components/graph/PlotlyLine";

import TimeSeries from "@/components/graph/TimeSeries";
import DataTable from "@/components/preprocess/DataTable";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import { eventBus } from "@/main";

export default {
  data() {
    return {
      dialog: false,
      column: null,
      graphReady: false
    };
  },
  watch: {
    // dialog: function(data) {
    //   if (data == false) {
    //     this.resetSeries();
    //     console.log("reset");
    //   }
    // }
  },
  props: [],

  components: {
    TimeSeries,
    DataTable,
    PlotlyLine
  },
  computed: {
    ...mapState("initialData", ["columns"]),

    ...mapGetters("initialData", ["indexNum"])
  },
  methods: {
    hideEditModal() {
      this.dialog = false;
    }
  },
  created() {
    eventBus.$on("openEditModal", column => {
      this.dialog = true;
      this.column = column;
    });
  },
  mounted() {
    console.log("editmodal mounted");
  }
};
</script>
