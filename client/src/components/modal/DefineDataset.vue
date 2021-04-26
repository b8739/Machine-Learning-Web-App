<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="400px">
      <!-- <template v-slot:activator="{ on, attrs }">
        <v-btn color="" v-bind="attrs" v-on="on">
          Define Dataset
        </v-btn>
      </template> -->
      <v-card>
        <v-container fluid>
          <span class="headline">Define Dataset</span>
          <!-- 최상단 메뉴 탭 -->

          <v-text-field
            v-model="tableName"
            :counter="10"
            label="Name of Dataset"
            required
          ></v-text-field>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="gray darken-1" text>
              Close
            </v-btn>
            <v-btn color="blue darken-1" @click.once="dataUpload" text>
              Confirm
            </v-btn>
          </v-card-actions>
        </v-container>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import axios from "axios";
import { eventBus } from "@/main";
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      dialog: false,
      tableName: "",
      formData: null
    };
  },
  methods: {
    ...mapMutations("initialData", ["loadSummarizedInfo"]),
    dataUpload() {
      axios
        .post("http://localhost:5000/dataupload", this.formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          params: {
            tableName: this.tableName
          }
        })
        .then(response => {
          this.result = response.data;
          this.loadSummarizedInfo(this.result);

          this.$router.push({ name: "dataSummary" });
        })
        .catch(ex => {
          console.log("ERR!!!!! : ", ex);
          // this.$router.push('/dataSummary'); //delete later
        });
    }
  },
  created() {
    eventBus.$on("openDefineDataset", modalStatus => {
      this.dialog = modalStatus;
    });
    eventBus.$on("formData", formData => {
      this.formData = formData;
    });
  }
};
</script>
