<template>
  <div class="text-center">
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="secondary" dark v-bind="attrs" v-on="on">
          Save Option
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
export default {
  data() {
    return {
      items: [{ title: "Overwrite" }, { title: "Save as New Dataset" }],
      dialog: false
    };
  },
  components: { DefineDataset },
  methods: {
    clickSaveOptionEvent(index) {
      if (index == 0) {
        this.saveTableAxios("overwrite");
      } else {
        // this.saveTableAxios("newDataset");
        this.dialog = true;
        eventBus.$emit("saveNewFileMode", this.dialog);
      }
    },
    saveTableAxios(saveOption) {
      const path = "http://localhost:5000/saveTable";
      axios
        .get(path, {
          params: {
            saveOption: saveOption
          }
        })
        .then(res => {
          console.log(res);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>
