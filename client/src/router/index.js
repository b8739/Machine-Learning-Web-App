import "@/assets/css/main.css";
import Vue from "vue";
import VueRouter from "vue-router";
import Projects from "../views/Projects";
import Datasets from "../views/Datasets";
import ModelingResult from "../views/modeling/ModelingResult";
import SimulationResult from "../views/simulation/SimulationResult";
import LoginForm from "@/components/login/LoginForm";
//lazyloading cancel (eda를 modeling에서도 봐야하므로)
// import Preprocess from "@/views/Preprocess";
// import Models from "@/views/modeling/Models";
// import Simulations from "@/views/simulation/Simulations";
// import ModelingProcess from "@/views/modeling/ModelingProcess";

// lazyloading
const Preprocess = () => import(/* webpackChunkName: "preprocess" */ "../views/Preprocess");
const Models = () => import(/* webpackChunkName: "models" */ "../views/modeling/Models");
const Simulations = () =>
  import(/* webpackChunkName: "simulations" */ "../views/simulation/Simulations");
const ModelingProcess = () =>
  import(/* webpackChunkName: "modelingProcess" */ "../views/modeling/ModelingProcess");

Vue.use(VueRouter); //Vue Router를 사용했다고 선언

const router = new VueRouter({
  mode: "history",

  routes: [
    {
      path: "/",
      component: LoginForm,
      props: true
    },
    {
      path: "/projects",
      component: Projects,
      props: true
    },
    {
      path: "/datasets",
      name: "datasets",
      component: Datasets,
      props: true
    },
    {
      path: "/preprocess",
      name: "preprocess",
      component: Preprocess,
      props: true
    },

    {
      path: "/models",
      component: Models,
      props: true
    },
    {
      path: "/modelingProcess",
      name: "modelingProcess",
      component: ModelingProcess,
      props: true
    },
    {
      path: "/simulations",
      name: "simulations",
      component: Simulations,
      props: true
    },
    {
      path: "/simulation/result",
      name: "simulationResult",
      component: SimulationResult,
      props: true
    },

    {
      path: "/modelingResult/:case",
      name: "modelingResult",
      component: ModelingResult,
      props: true
    }
    // {
    //   path: "/modelingSingleResult/:case",
    //   name: "modelingSingleResult",
    //   component: ModelingSingleResult,
    //   props: true
    // }
  ]
});

export default router;
