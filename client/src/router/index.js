import Vue from 'vue';
import VueRouter from 'vue-router';
import FileUploader from "../views/FileUploader";
import DataSummary from "../views/DataSummary";
import '../assets/css/main.css';

// import Login from "../views/Login";

Vue.use(VueRouter); //View Router를 사용했다고 선언

const router = new VueRouter({
    mode:"history",

    routes:[
    // {
    //     path:"/", 
    //     name:"login", 
    //     component: Login,
    //     props:true
    // },
    {
        path:"/", 
        component: FileUploader,
        props:true
    },
    {
        path:"/dataSummary", 
        name:"dataSummary", 
        component: DataSummary,
        props:true
    },

    ]
});

export default router;