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
  </div>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      items: [{ title: "Overwrite" }, { title: "Save as New Dataset" }]
    };
  },
  methods: {
    clickSaveOptionEvent(index) {
      if (index == 0) {
        this.saveTableAxios("overwrite");
      } else {
        this.saveTableAxios("newDataset");
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
