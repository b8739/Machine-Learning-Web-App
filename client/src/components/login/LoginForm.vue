<template>
  <v-app id="inspire">
    <!-- <v-btn @click="mongoTest">mongoTest</v-btn> -->
    <v-main>
      <v-card>
        <!-- <v-subheader> Last AWS Update: {{ uploadDate }} </v-subheader> -->
        <v-subheader> Last AWS Update: 2021-12-15 09:48 PM</v-subheader>
      </v-card>
      <v-container fluid fill-height>
        <v-row align="center" justify="center">
          <v-col xs="12" sm="8" md="4">
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Login</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    prepend-icon="person"
                    name="login"
                    label="Login"
                    type="text"
                  ></v-text-field>
                  <v-text-field
                    id="password"
                    prepend-icon="lock"
                    name="password"
                    label="Password"
                    type="password"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" to="/projects">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";

export default {
  name: "Login",
  data() {
    return {};
  },
  props: {
    source: String
  },
  computed: {
    uploadDate() {
      let date = new Date()
        .toISOString()
        .substr(0, 10)
        .replace("T", " ");
      let today = new Date();

      let hours = today.getHours(); // 시
      let minutes = today.getMinutes(); // 분

      return date + " " + hours + ":" + minutes;
    }
  },
  methods: {
    // ...mapMutations("initialData", ["resetState"])
    ...mapActions("initialData", ["resetAllState"]),
    mongoTest() {
      let path = "http://localhost:8000/test";
      // axios
      this.$axios({
        method: "get",
        url: path
      })
        .then(res => {
          console.log(res.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  created() {
    console.log("hi");
    // this.resetState();
    this.resetAllState();
  }
};
</script>

<style></style>
