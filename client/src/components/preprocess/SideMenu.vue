<template>
  <v-container>
    <v-navigation-drawer height="100vh" v-model="drawer" absolute :mini-variant.sync="mini">
      <v-list-item class="mt-10 px-2">
        <v-list-item-avatar>
          <v-img src="https://randomuser.me/api/portraits/men/85.jpg"></v-img>
        </v-list-item-avatar>

        <v-list-item-title>User123</v-list-item-title>

        <v-btn icon @click.stop="mini = !mini">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>
      <v-list dense>
        <!-- <v-list-group v-model="activeState">
          <template v-slot:activator>
            <v-list-item-title>Current Dataset</v-list-item-title>
          </template>

          <v-select
            class="px-3"
            outlined
            clearable
            hide-details
            dense
            :label="tableName"
            :items="tableList"
          ></v-select>
        </v-list-group> -->
      </v-list>
      <keep-alive>
        <component v-bind:is="dynamicSideMenu"></component>
      </keep-alive>

      <!-- 구분선 -->
      <!-- <v-divider class=""></v-divider> -->
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import TableSideMenu from "@/components/sideMenu/TableSideMenu";
import SummarySideMenu from "@/components/sideMenu/SummarySideMenu";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import { eventBus } from "@/main";
import axios from "axios";
export default {
  data() {
    return {
      drawer: true,
      mini: false,

      tableItems: [
        { title: "Add Feature", icon: "mdi-plus" },
        { title: "Update Feature", icon: "mdi-pencil" },
        { title: "Delete Row", icon: "mdi-delete" }
      ],

      activeState: true,
      currentComponent: "SummaryTable"
      // currentComponent: "DataTable"
    };
  },
  components: {
    TableSideMenu,
    SummarySideMenu
  },
  computed: {
    ...mapState({
      tableName: state => state.initialData.tableName,
      projectName: state => state.initialData.projectName,

      tableList: state => state.initialData.tableList
    }),
    dataFeatures() {
      return this.$root.$refs.dataFeatures;
    },
    infiniteTable() {
      return this.$root.$refs.infiniteTable;
    },

    dynamicSideMenu() {
      if (this.currentComponent == "SummaryTable") return "SummarySideMenu";
      else return "TableSideMenu";
    }
  },
  methods: {
    ...mapMutations("initialData", ["loadTableList"]),
    ...mapMutations("initialData", ["resetState"]),
    ...mapActions("initialData", ["loadSummarizedData"]),
    ...mapMutations("initialData", ["setTableName"]),
    ...mapMutations("dataTableHandler", ["resetDataTableVuex"]),
    ...mapMutations("preprocessHandler", ["resetPreprocessVuex"]),
    ...mapActions("initialData", ["loadColumns"]),
    ...mapActions("initialData", ["loadDatasetSize"]),
    ...mapActions("summaryTableHandler", ["cloneOriginalArray"]),
    ...mapActions("apexchartGraph", ["loadFeatureGraphData"]),

    clickTableNameEvent(tableName) {
      this.resetState();
      this.setTableName(tableName);
      this.loadSummarizedData();
      this.loadColumns();
      this.loadDatasetSize();
      this.showTables(projectName);
      this.resetDataTableVuex();
      this.resetPreprocessVuex();
      eventBus.$emit("reloadDataTable", true);

      this.selectionTimer = setTimeout(() => {
        this.loadFeatureGraphData();

        this.cloneOriginalArray();
      }, 1000);
    },

    showTables() {
      let path = "http://atticmlapp.ap-northeast-2.elasticbeanstalk.com/showTables";
      axios({
        method: "post",
        url: path,
        data: { projectName: this.projectName }
      })
        .then(res => {
          this.loadTableList(res.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    this.showTables();
    eventBus.$on("changeComponent", componentName => {
      this.currentComponent = componentName;
    });
  },
  mounted() {
    this.showTables();
  }
};
</script>
