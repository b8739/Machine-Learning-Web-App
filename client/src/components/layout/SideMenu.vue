<template>
  <v-container>
    <v-navigation-drawer v-model="drawer" absolute>
      <v-list-item class="px-2">
        <v-list-item-title>Options</v-list-item-title>
        <v-btn icon @click.stop="mini = !mini">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense>
        <v-list-item v-for="item in items" :key="item.title" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <DeleteRowModal />
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import DeleteRowModal from "@/components/modal/DeleteRowModal";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      drawer: true,
      items: [
        { title: "Add Column", icon: "mdi-plus-circle-outline" },
        { title: "Update Column", icon: "mdi-select-drag" }
      ]
    };
  },
  components: {
    DeleteRowModal
  },
  // methods: {
  //   hideDrawer() {
  //     this.drawer = !this.drawer;
  //   }
  // },
  created() {
    // eventBus.$on("showDrawer", drawerStatus => {
    //   this.drawer = drawerStatus;
    //   console.log(drawerStatus);
    // });
  }
};
</script>
