<template>
  <v-container>
    <v-navigation-drawer v-model="drawer" absolute>
      <v-list-item class="px-2">
        <v-list-item-avatar>
          <v-img src="https://randomuser.me/api/portraits/men/85.jpg"></v-img>
        </v-list-item-avatar>

        <v-list-item-title>John Leider</v-list-item-title>

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
    </v-navigation-drawer>
  </v-container>
</template>

<script>
import { eventBus } from "@/main";
export default {
  data() {
    return {
      drawer: true,
      items: [
        { title: "Home", icon: "mdi-view-dashboard" },
        { title: "About", icon: "mdi-forum" }
      ]
    };
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
